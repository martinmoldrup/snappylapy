"""Snapshot repporter, combining from multiple files in syrupy  and snappylapy."""
from itertools import zip_longest
from typing import (
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Union,
    Sequence,
    Any,
)
import json
import os
from dataclasses import dataclass, field
from difflib import ndiff
from contextlib import contextmanager


SerializedData = Union[str, bytes]

DISABLE_COLOR_ENV_VAR = "ANSI_COLORS_DISABLED"
SYMBOL_ELLIPSIS = "..."  # U+2026
SYMBOL_NEW_LINE = "␤"  # U+2424
SYMBOL_CARRIAGE = "␍"  # U+240D
DIFF_LINE_COUNT_LIMIT = 100
DIFF_LINE_WIDTH_LIMIT = 1000
DISABLE_COLOR_ENV_VARS = {DISABLE_COLOR_ENV_VAR, "NO_COLOR"}

def set_attrs(obj: Any, attrs: Dict[str, Any]) -> Any:
    for k in attrs:
        setattr(obj, k, attrs[k])

def qdiff(
    lines_a: "Sequence[str]",
    lines_b: "Sequence[str]",
    *,
    line_diff_limit: int = DIFF_LINE_COUNT_LIMIT,
    line_size_limit: int = DIFF_LINE_WIDTH_LIMIT,
) -> "Iterator[str]":
    """
    Wrapper around difflib ndiff to bail early
    https://github.com/python/cpython/issues/65452
    """
    first_diff_line_idx = 0
    first_diff_char_idx = 0

    for i in range(max(len(lines_a), len(lines_b))):
        line_a = "".join(lines_a[i : i + 1])  # noqa E203
        line_b = "".join(lines_b[i : i + 1])  # noqa E203
        if line_a != line_b:
            first_diff_line_idx = i
            for j in range(max(len(line_a), len(line_b))):
                char_a = line_a[j : j + 1]  # noqa E203
                char_b = line_b[j : j + 1]  # noqa E203
                if char_a != char_b:
                    first_diff_char_idx = j
                    break
            break

    def adjust_lines(lines: "Sequence[str]") -> "Sequence[str]":
        line_idx_from = max(first_diff_line_idx - line_diff_limit, 0)
        line_idx_to = first_diff_line_idx + line_diff_limit

        symbol_hidden_line = SYMBOL_ELLIPSIS + SYMBOL_ELLIPSIS
        return (
            # include an indicator in the diff if this was not the first line
            ([symbol_hidden_line] if line_idx_from > 0 else [])
            # show included lines with the ends truncated off
            + [
                adj_line
                for n, line in enumerate(lines[line_idx_from:line_idx_to])
                # adjust the first line shown to be from the first different spotted
                for line_start, line_end in [
                    (
                        (
                            max(first_diff_char_idx - line_size_limit, 0)
                            if n == line_idx_from
                            else 0
                        ),
                        (
                            first_diff_char_idx + line_size_limit
                            if n == line_idx_from
                            else line_size_limit
                        ),
                    ),
                ]
                for adj_line in [
                    (SYMBOL_ELLIPSIS if line_start > 0 else "")
                    + line[line_start:line_end]
                    + (SYMBOL_ELLIPSIS if line_end < len(line) else "")
                ]
            ]
            # include an indicator in the diff if this was not the last line
            + ([symbol_hidden_line] if line_idx_to < len(lines) else [])
        )

    return ndiff(adjust_lines(lines_a), adjust_lines(lines_b))


@contextmanager
def env_context(**kwargs: str) -> Iterator[None]:
    prev_env = {**os.environ}
    try:
        yield os.environ.update(kwargs)
    finally:
        os.environ.clear()
        os.environ.update(prev_env)

@contextmanager
def obj_attrs(obj: Any, attrs: Dict[str, Any]) -> Iterator[None]:
    prev_attrs = {k: getattr(obj, k, None) for k in attrs}
    try:
        yield set_attrs(obj, attrs)
    finally:
        set_attrs(obj, prev_attrs)
    
def get_env_value(env_var_name: str) -> object:
    try:
        return json.loads(os.environ[env_var_name])
    except (KeyError, TypeError, json.decoder.JSONDecodeError):
        return os.environ.get(env_var_name)

@dataclass
class DiffedLine:
    a: Optional[str] = None
    b: Optional[str] = None
    c: List[str] = field(default_factory=list)
    diff_a: str = ""
    diff_b: str = ""

    @property
    def has_snapshot(self) -> bool:
        return self.a is not None

    @property
    def has_received(self) -> bool:
        return self.b is not None

    @property
    def is_complete(self) -> bool:
        return self.has_snapshot and self.has_received

    @property
    def is_context(self) -> bool:
        return bool(self.c)


def _is_color_disabled() -> bool:
    return any(map(get_env_value, DISABLE_COLOR_ENV_VARS))

def _count_leading_whitespace(s: str) -> int:
    return len(s) - len(s.lstrip())

@dataclass
class TerminalCodes:
    ESC: str = "\x1b["
    END: str = "m"
    FOREGROUND_256: str = f"{ESC}38;5;"
    BACKGROUND_256: str = f"{ESC}48;5;"

    STYLES = {
        "bold": "1",
        "dim": "2",
        "italic": "3",
        "underline": "4",
        "reset": "0",
    }

    COLORS = {
        "black": "0",
        "red": "1",
        "green": "2",
        "yellow": "3",
    }


def _attr(style: str) -> str:
    if _is_color_disabled():
        return ""
    return f"{TerminalCodes.ESC}{TerminalCodes.STYLES[style]}{TerminalCodes.END}"


def _fg(color: Union[int, str]) -> str:
    if _is_color_disabled():
        return ""
    color_code = TerminalCodes.COLORS[color] if isinstance(color, (str,)) else color
    return f"{TerminalCodes.FOREGROUND_256}{str(color_code)}{TerminalCodes.END}"


def _bg(color: int) -> str:
    if _is_color_disabled():
        return ""
    return f"{TerminalCodes.BACKGROUND_256}{str(color)}{TerminalCodes.END}"


def _stylize(text: Union[str, int], formatting: str) -> str:
    if _is_color_disabled():
        return str(text)
    return f"{formatting}{text}{_attr('reset')}"


def reset(text: Union[str, int]) -> str:
    return _stylize(text, _attr("reset"))


def red(text: Union[str, int]) -> str:
    return _stylize(text, _fg("red"))


def yellow(text: Union[str, int]) -> str:
    return _stylize(text, _fg("yellow"))


def green(text: Union[str, int]) -> str:
    return _stylize(text, _fg("green"))


def bold(text: Union[str, int]) -> str:
    return _stylize(text, _attr("bold"))


def error_style(text: Union[str, int]) -> str:
    return bold(red(text))


def warning_style(text: Union[str, int]) -> str:
    return bold(yellow(text))


def success_style(text: Union[str, int]) -> str:
    return bold(green(text))


def snapshot_style(text: Union[str, int]) -> str:
    return _stylize(text, _bg(225) + _fg(90))


def snapshot_diff_style(text: Union[str, int]) -> str:
    return _stylize(text, _bg(90) + _fg(225))


def received_style(text: Union[str, int]) -> str:
    return _stylize(text, _bg(195) + _fg(23))


def received_diff_style(text: Union[str, int]) -> str:
    return _stylize(text, _bg(23) + _fg(195))


def context_style(text: Union[str, int]) -> str:
    return _stylize(text, _attr("dim"))

class SnapshotReporter:
    _context_line_count = 1

    def diff_snapshots(
        self, serialized_data: "SerializedData", snapshot_data: "SerializedData"
    ) -> "SerializedData":
        env = {DISABLE_COLOR_ENV_VAR: "true"}
        attrs = {"_context_line_count": 0}
        with env_context(**env), obj_attrs(self, attrs):
            return "\n".join(self.diff_lines(serialized_data, snapshot_data))

    def diff_lines(
        self, serialized_data: "SerializedData", snapshot_data: "SerializedData"
    ) -> Iterator[str]:
        for line in self.__diff_lines(str(snapshot_data), str(serialized_data)):
            yield reset(line)

    @property
    def _ends(self) -> Dict[str, str]:
        return {"\n": self._marker_new_line, "\r": self._marker_carriage}

    @property
    def _context_line_max(self) -> int:
        return self._context_line_count * 2

    @property
    def _marker_context_max(self) -> str:
        return SYMBOL_ELLIPSIS

    @property
    def _marker_new_line(self) -> str:
        return SYMBOL_NEW_LINE

    @property
    def _marker_carriage(self) -> str:
        return SYMBOL_CARRIAGE

    def __diff_lines(self, a: str, b: str) -> Iterator[str]:
        for line in self.__diffed_lines(a, b):
            show_ends = (
                self.__strip_ends(line.a[1:] if line.a is not None else "")
                == self.__strip_ends(line.b[1:] if line.b is not None else "")
                if line.is_complete
                else False
            )
            if line.has_snapshot and line.a is not None:
                yield self.__format_line(
                    line.a, line.diff_a, snapshot_style, snapshot_diff_style, show_ends
                )
            if line.has_received and line.b is not None:
                yield self.__format_line(
                    line.b, line.diff_b, received_style, received_diff_style, show_ends
                )
            yield from map(context_style, self.__limit_context(line.c))

    def __diffed_lines(self, a: str, b: str) -> Iterator["DiffedLine"]:
        staged_diffed_line: Optional[DiffedLine] = None
        for line in qdiff(a.splitlines(keepends=True), b.splitlines(keepends=True)):
            is_context_line = line[0] == " "
            is_snapshot_line = line[0] == "-"
            is_received_line = line[0] == "+"
            is_diff_line = line[0] == "?"

            if is_context_line or is_diff_line:
                line = self.__strip_ends(line)

            if staged_diffed_line:
                if is_diff_line:
                    if staged_diffed_line.has_received:
                        staged_diffed_line.diff_b = line
                    elif staged_diffed_line.has_snapshot:
                        staged_diffed_line.diff_a = line
                    # else: should never happen because then it would have
                    # encounted a diff line without any previously staged line
                else:
                    should_unstage = (
                        staged_diffed_line.is_complete
                        or (staged_diffed_line.has_snapshot and is_snapshot_line)
                        or (staged_diffed_line.has_received and is_received_line)
                        or (staged_diffed_line.is_context and not is_context_line)
                    )
                    if should_unstage:
                        yield staged_diffed_line
                        staged_diffed_line = None
                    elif is_snapshot_line:
                        staged_diffed_line.a = line
                    elif is_received_line:
                        staged_diffed_line.b = line
                    elif is_context_line:
                        staged_diffed_line.c.append(line)

            if not staged_diffed_line:
                if is_snapshot_line:
                    staged_diffed_line = DiffedLine(a=line)
                elif is_received_line:
                    staged_diffed_line = DiffedLine(b=line)
                elif is_context_line:
                    staged_diffed_line = DiffedLine(c=[line])
                # else: should never happen because then it would have
                # encounted a diff line without any previously staged line

        if staged_diffed_line:
            yield staged_diffed_line

    def __format_line(
        self,
        line: str,
        diff_markers: str,
        line_style: Callable[[str], str],
        diff_style: Callable[[str], str],
        show_ends: bool,
    ) -> str:
        if show_ends:
            for old, new in self._ends.items():
                line = line.replace(old, new)
        else:
            line = self.__strip_ends(line)
        return "".join(
            diff_style(char) if str(marker) in "-+^" else line_style(char)
            for marker, char in zip_longest(diff_markers.rstrip(), line)
            if char is not None
        )

    def __limit_context(self, lines: List[str]) -> Iterator[str]:
        yield from lines[: self._context_line_count]
        num_lines = len(lines)
        if num_lines:
            if num_lines > self._context_line_max:
                if self._context_line_count:
                    num_space = (
                        _count_leading_whitespace(lines[self._context_line_count - 1])
                        + _count_leading_whitespace(lines[-self._context_line_count])
                    ) // 2
                else:
                    num_space = _count_leading_whitespace(lines[num_lines // 2])
                yield " " * num_space + self._marker_context_max
            if self._context_line_count and num_lines > 1:
                yield from lines[-self._context_line_count :]  # noqa: E203

    def __strip_ends(self, line: str) -> str:
        return line.rstrip("".join(self._ends.keys()))


if __name__ == "__main__":
    reporter = SnapshotReporter()
    serialized_data = json.dumps({"name": "John Doe", "age": 31}, indent=2)
    snapshot_data = json.dumps({"name": "John Doe", "age": 32}, indent=2)
    print(reporter.diff_snapshots(serialized_data, snapshot_data))