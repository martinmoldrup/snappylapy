"""Snapshot testing for Python."""
from __future__ import annotations

import inspect
import pathlib
from .serialization import BytesSerializer, JsonPickleSerializer, StringSerializer
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar


@dataclass
class Settings:
    """Shared setting for all the strategies for doing snapshot testing."""

    snapshot_dir: pathlib.Path = pathlib.Path("__snapshots__")
    test_results_dir: pathlib.Path = pathlib.Path("__test_results__")
    snapshot_update: bool = False
    filename_base: str = "no_filename"
    filename_extension: str = "txt"

    @property
    def filename(self) -> str:
        """Get the snapshot filename."""
        return f"{self.filename_base}.{self.filename_extension}"


T = TypeVar("T")


class BaseSnapshot(ABC, Generic[T]):
    """Base class for snapshot testing."""

    def __init__(
        self,
        update_snapshots: bool,  # noqa: FBT001
        settings: Settings,
    ) -> None:
        """Initialize the base snapshot."""
        self.settings = settings
        self.snapshot_update: bool = update_snapshots
        self._data: T | None = None

    def to_match_snapshot(self) -> None:
        """Assert test results match the snapshot."""
        if not self._compare_snapshot():
            error_msg = "Test results do not match the snapshot."
            raise AssertionError(error_msg)

    def _prepare_test(self, data: T, name: str, extension: str) -> None:
        """Prepare and save test results."""
        self._data = data
        if not name:
            name = self._get_filename_base()
        self.settings.filename_base = name
        self.settings.filename_extension = extension
        file_path = self.settings.test_results_dir / self.settings.filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        self._save_test_results(file_path, data)

    def _compare_snapshot(self) -> bool:
        """Compare the snapshot with test results, updating if needed."""
        if not self.snapshot_update and not (self.settings.snapshot_dir /
                                             self.settings.filename).exists():
            error_msg = f"Snapshot file not found: {self.settings.filename}, run pytest with the --snapshot-update flag to create it."  # noqa: E501
            raise FileNotFoundError(error_msg)
        if self.snapshot_update:
            self._update_snapshot()
        snapshot_data = self._read_file(self.settings.snapshot_dir /
                                        self.settings.filename)
        test_data = self._read_file(self.settings.test_results_dir /
                                    self.settings.filename)
        return snapshot_data == test_data

    def _update_snapshot(self) -> None:
        """Write test results to the snapshot file."""
        snap_path = self.settings.snapshot_dir / self.settings.filename
        test_path = self.settings.test_results_dir / self.settings.filename
        snap_path.parent.mkdir(parents=True, exist_ok=True)
        snap_path.write_bytes(test_path.read_bytes())

    def _read_file(self, path: pathlib.Path) -> bytes:
        """Read file bytes or return placeholder."""
        return path.read_bytes() if path.exists() else b"<No file>"

    def _get_filename_base(self) -> str:
        """Derive a filename from the call stack."""
        frame = inspect.currentframe()
        while frame:
            if frame.f_code.co_filename != __file__:
                return frame.f_code.co_name
            frame = frame.f_back
        error_msg = "Could not derive filename from stack."
        raise ValueError(error_msg)

    @abstractmethod
    def _save_test_results(self, path: pathlib.Path, data: T) -> None:
        """Save data for test results."""
        raise NotImplementedError


class DictExpect(BaseSnapshot[dict]):
    """Snapshot testing for dictionaries."""

    def __call__(self,
                 data_to_snapshot: dict,
                 name: str = "",
                 filetype: str = "dict.json") -> DictExpect:
        """Prepare a dictionary for snapshot testing."""
        self._prepare_test(data_to_snapshot, name, filetype)
        return self

    def _save_test_results(self, path: pathlib.Path, data: dict) -> None:
        """Save dictionary data to a file."""
        data_bin = JsonPickleSerializer[dict]().serialize(data)
        path.write_bytes(data_bin)


class ListExpect(BaseSnapshot[list[Any]]):
    """Snapshot testing for lists."""

    def __call__(
        self,
        data_to_snapshot: list[Any],
        name: str = "",
        filetype: str = "list.json",
    ) -> ListExpect:
        """Prepare a list for snapshot testing."""
        self._prepare_test(data_to_snapshot, name, filetype)
        return self

    def _save_test_results(
        self,
        path: pathlib.Path,
        data: list[Any],
    ) -> None:
        """Save list data to a file."""
        data_bin = JsonPickleSerializer[list[Any]]().serialize(data)
        path.write_bytes(data_bin)


class StringExpect(BaseSnapshot[str]):
    """Snapshot testing for strings."""

    def __call__(self,
                 data_to_snapshot: str,
                 name: str = "",
                 filetype: str = "string.txt") -> StringExpect:
        """Prepare a string for snapshot testing."""
        self._prepare_test(data_to_snapshot, name, filetype)
        return self

    def _save_test_results(self, path: pathlib.Path, data: str) -> None:
        """Save string data to a file."""
        data_bin = StringSerializer().serialize(data)
        path.write_bytes(data_bin)


class BytesExpect(BaseSnapshot[bytes]):
    """Snapshot testing for bytes."""

    def __call__(self,
                 data_to_snapshot: bytes,
                 name: str = "",
                 filetype: str = "bytes.txt") -> BytesExpect:
        """Prepare bytes for snapshot testing."""
        self._prepare_test(data_to_snapshot, name, filetype)
        return self

    def _save_test_results(self, path: pathlib.Path, data: bytes) -> None:
        """Save bytes data to a file."""
        data_bin = BytesSerializer().serialize(data)
        path.write_bytes(data_bin)


class Expect:
    """Snapshot testing class."""

    def __init__(
            self,
            update_snapshots: bool,  # noqa: FBT001
    ) -> None:
        """Initialize the snapshot testing."""
        self.settings = Settings()
        self.dict = DictExpect(update_snapshots, self.settings)
        self.list = ListExpect(update_snapshots, self.settings)
        self.string = StringExpect(update_snapshots, self.settings)
        self.bytes = BytesExpect(update_snapshots, self.settings)

    def read_snapshot(self) -> bytes:
        """Read the snapshot file."""
        return (self.settings.snapshot_dir /
                self.settings.filename).read_bytes()

    def read_test_results(self) -> bytes:
        """Read the test results file."""
        return (self.settings.test_results_dir /
                self.settings.filename).read_bytes()

    @property
    def snapshot_dir(self) -> pathlib.Path:
        """Get the snapshot directory."""
        return self.settings.snapshot_dir

    @snapshot_dir.setter
    def snapshot_dir(self, value: str | pathlib.Path) -> None:
        """Set the snapshot directory."""
        self.settings.snapshot_dir = pathlib.Path(value) if isinstance(
            value, str) else value

    @property
    def test_results_dir(self) -> pathlib.Path:
        """Get the test results directory."""
        return self.settings.test_results_dir

    @test_results_dir.setter
    def test_results_dir(self, value: str | pathlib.Path) -> None:
        """Set the test results directory."""
        self.settings.test_results_dir = pathlib.Path(value) if isinstance(
            value, str) else value


class LoadSnapshot:
    """Snapshot loading class."""

    def __init__(self, settings: Settings) -> None:
        """Initialize the snapshot loading."""
        self.settings = settings

    def _read_snapshot(self) -> bytes:
        """Read the snapshot file."""
        return (self.settings.snapshot_dir /
                self.settings.filename).read_bytes()

    def dict(self) -> dict:
        """Load dictionary snapshot."""
        self.settings.filename_extension = "dict.json"
        return JsonPickleSerializer[dict]().deserialize(self._read_snapshot())

    def list(self) -> list[Any]:
        """Load list snapshot."""
        self.settings.filename_extension = "list.json"
        return JsonPickleSerializer[list[Any]]().deserialize(
            self._read_snapshot())

    def string(self) -> str:
        """Load string snapshot."""
        self.settings.filename_extension = "string.txt"
        return StringSerializer().deserialize(self._read_snapshot())

    def bytes(self) -> bytes:
        """Load bytes snapshot."""
        self.settings.filename_extension = "bytes.txt"
        return BytesSerializer().deserialize(self._read_snapshot())
