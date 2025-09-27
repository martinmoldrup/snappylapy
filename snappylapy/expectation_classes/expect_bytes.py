"""Snapshot testing and expectations for bytes."""

from __future__ import annotations

import re
from collections.abc import Iterable

from .base_snapshot import BaseSnapshot
from snappylapy.serialization import BytesSerializer


class BytesExpect(BaseSnapshot[bytes]):
    """Snapshot testing for bytes."""

    serializer_class = BytesSerializer

    def __call__(self, data_to_snapshot: bytes, name: str | None = None, filetype: str = "bytes.txt") -> BytesExpect:
        """Prepare bytes for snapshot testing."""
        self._prepare_test(data_to_snapshot, name, filetype)
        return self

    def to_be(self, expected: bytes) -> None:
        """Assert that the bytes equals the expected bytes."""
        actual = self._ensure_data_available()
        assert actual == expected

    def to_equal(self, expected: bytes) -> None:
        """Assert that the bytes equals the expected bytes."""
        actual = self._ensure_data_available()
        assert actual == expected

    def to_contain(self, subsequence: bytes) -> None:
        """Assert that the bytes contains the given subsequence."""
        actual = self._ensure_data_available()
        if subsequence not in actual:
            msg = f"Expected bytes to contain {subsequence!r}"
            raise AssertionError(msg)

    def to_not_contain(self, subsequence: bytes) -> None:
        """Assert that the bytes does not contain the given subsequence."""
        actual = self._ensure_data_available()
        if subsequence in actual:
            msg = f"Expected bytes to not contain {subsequence!r}"
            raise AssertionError(msg)

    def to_start_with(self, prefix: bytes) -> None:
        """Assert that the bytes starts with the given prefix."""
        actual = self._ensure_data_available()
        if not actual.startswith(prefix):
            msg = f"Expected bytes to start with {prefix!r}"
            raise AssertionError(msg)

    def to_end_with(self, suffix: bytes) -> None:
        """Assert that the bytes ends with the given suffix."""
        actual = self._ensure_data_available()
        if not actual.endswith(suffix):
            msg = f"Expected bytes to end with {suffix!r}"
            raise AssertionError(msg)

    def to_have_length(self, expected_length: int) -> None:
        """Assert that the bytes has the expected length."""
        actual = self._ensure_data_available()
        actual_length = len(actual)
        if actual_length != expected_length:
            msg = f"Expected bytes length {expected_length} but got {actual_length}"
            raise AssertionError(msg)

    def to_be_empty(self) -> None:
        """Assert that the bytes is empty."""
        actual = self._ensure_data_available()
        if actual:
            msg = "Expected bytes to be empty"
            raise AssertionError(msg)

    def to_not_be_empty(self) -> None:
        """Assert that the bytes is not empty."""
        actual = self._ensure_data_available()
        if not actual:
            msg = "Expected bytes to not be empty"
            raise AssertionError(msg)

    def to_decode_as(self, expected_string: str, encoding: str = "utf-8") -> None:
        """Assert that the bytes decodes to the expected string."""
        actual = self._ensure_data_available()
        try:
            decoded = actual.decode(encoding)
            if decoded != expected_string:
                msg = f"Expected bytes to decode to {expected_string!r} but got {decoded!r}"
                raise AssertionError(msg)
        except UnicodeDecodeError as error:
            msg = f"Failed to decode bytes as {encoding}: {error}"
            raise AssertionError(msg) from error

    def to_match_regex_when_decoded(self, pattern: str, encoding: str = "utf-8", flags: int = 0) -> None:
        """Assert that the bytes, when decoded, matches the given regex pattern."""
        actual = self._ensure_data_available()
        try:
            decoded = actual.decode(encoding)
            if not re.search(pattern, decoded, flags):
                msg = f"Expected decoded bytes to match regex pattern '{pattern}'"
                raise AssertionError(msg)
        except UnicodeDecodeError as error:
            msg = f"Failed to decode bytes as {encoding}: {error}"
            raise AssertionError(msg) from error

    def to_contain_any_of(self, subsequences: Iterable[bytes]) -> None:
        """Assert that the bytes contains at least one of the given subsequences."""
        actual = self._ensure_data_available()
        subsequence_list = list(subsequences)
        if not any(subseq in actual for subseq in subsequence_list):
            msg = f"Expected bytes to contain at least one of {subsequence_list!r}"
            raise AssertionError(msg)

    def to_contain_all_of(self, subsequences: Iterable[bytes]) -> None:
        """Assert that the bytes contains all of the given subsequences."""
        actual = self._ensure_data_available()
        subsequence_list = list(subsequences)
        missing = [subseq for subseq in subsequence_list if subseq not in actual]
        if missing:
            msg = f"Expected bytes to contain all subsequences, missing: {missing!r}"
            raise AssertionError(msg)

    def to_be_truthy(self) -> None:
        """Assert that the bytes evaluates to True."""
        actual = self._ensure_data_available()
        if not actual:
            msg = "Expected bytes to be truthy but it was falsy."
            raise AssertionError(msg)

    def to_be_falsy(self) -> None:
        """Assert that the bytes evaluates to False."""
        actual = self._ensure_data_available()
        if actual:
            msg = "Expected bytes to be falsy but it was truthy."
            raise AssertionError(msg)

    def _ensure_data_available(self) -> bytes:
        """Return the stored data ensuring it exists and is bytes."""
        if self._data is None:
            msg = "No bytes data prepared yet. Call the expectation with data first."
            raise RuntimeError(msg)
        if not isinstance(self._data, bytes):
            msg = f"Expected bytes data but received {type(self._data).__name__}."
            raise TypeError(msg)
        return self._data
