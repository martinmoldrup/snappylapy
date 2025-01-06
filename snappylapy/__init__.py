"""

"""
from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar
import pathlib
import inspect


T = TypeVar('T')


class BaseSnapshot(ABC, Generic[T]):
    DEFAULT_SNAPSHOTS_OUTPUT_DIR = pathlib.Path("__snapshots__")
    DEFAULT_test_results_dir = pathlib.Path("__test_results__")

    def __init__(self, update_snapshots: bool = False) -> None:
        self._snapshot_dir = self.DEFAULT_SNAPSHOTS_OUTPUT_DIR
        self.test_results_dir = self.DEFAULT_test_results_dir
        self.filename: str | None = None
        self.snapshot_update = update_snapshots
        self._element: T | None = None

    @property
    def snapshot_dir(self) -> pathlib.Path:
        return self._snapshot_dir

    @snapshot_dir.setter
    def snapshot_dir(self, value: str | pathlib.Path) -> None:
        if isinstance(value, str):
            self._snapshot_dir = pathlib.Path(value)
        elif isinstance(value, pathlib.Path):
            self._snapshot_dir = value
        else:
            raise ValueError("snapshot_dir must be a string or a pathlib.Path")

    def __eq__(self, value: object) -> bool:
        assert isinstance(value, bytes), "Only bytes are supported"
        self.__call__(data_to_snapshot=value)
        return self._exact_match_with_snapshot()

    def read_snapshot(self) -> bytes:
        snapshot_path = self.snapshot_dir / self.filename
        if not snapshot_path.exists():
            return b"<No snapshot>"
        return snapshot_path.read_bytes()

    def read_test_results(self) -> bytes:
        test_results_path = self.test_results_dir / self.filename
        if not test_results_path.exists():
            return b"<No test results>"
        return test_results_path.read_bytes()

    def get_filename(self, filetype: str) -> str:
        frame = inspect.currentframe()
        while frame:
            is_in_current_module = frame.f_code.co_filename == __file__
            if not is_in_current_module:
                return f"{frame.f_code.co_name}.{filetype}"
            frame = frame.f_back
        raise ValueError("Could not determine the filename from the stack")

    def __call__(self,
                 data_to_snapshot: T,
                 name: str = "",
                 filetype="txt") -> None:
        """Save the to the output directory."""
        self._element = data_to_snapshot
        if name:
            self.filename = f"{name}.{filetype}"
        else:
            self.filename = self.get_filename(filetype)
        output_path = self.test_results_dir / self.filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self._save_test_results(output_path, data_to_snapshot)

    @abstractmethod
    def _save_test_results(self, path: pathlib.Path, data: T) -> None:
        """Save the snapshot to the given path."""

    def _update_snapshot(self) -> None:
        snapshot_path = self.snapshot_dir / self.filename
        if self.snapshot_update or not snapshot_path.exists():
            test_results_path = self.test_results_dir / self.filename
            snapshot_path.parent.mkdir(parents=True, exist_ok=True)
            snapshot_path.write_bytes(test_results_path.read_bytes())


    def _exact_match_with_snapshot(self) -> bool:
        self._update_snapshot()
        return self.read_snapshot() == self.read_test_results()
    
    def assert_match(self, value: object, file_name: str) -> None:
        name, file_extension = file_name.split(".")
        self.__call__(data_to_snapshot=value, name=name, filetype=file_extension)
        return self._exact_match_with_snapshot()

    def assert_immutable(self):
        assert self._exact_match_with_snapshot()

    def to_match_snapshot(self) -> None:
        self.assert_immutable()

class SnapshotBytes(BaseSnapshot[bytes]):
    """The bytes implementation of the Snapshot class."""
    def _save_test_results(self, path: pathlib.Path, data: bytes) -> None:
        path.write_bytes(data)

class SnapshotString(BaseSnapshot[str]):
    """The bytes implementation of the Snapshot class."""
    def _save_test_results(self, path: pathlib.Path, data: str) -> None:
        path.write_text(data)


class Snapshot(BaseSnapshot):
    """The public interface for the Snapshot class."""
    def __init__(self, update_snapshots: bool = False) -> None:
        super().__init__(update_snapshots=update_snapshots)
        self._bytes: Optional[SnapshotBytes] = None
        self._str: Optional[SnapshotString] = None
    
    @property
    def bytes(self) -> SnapshotBytes:
        if self._bytes is None:
            self._bytes = SnapshotBytes(self._update_snapshot)
        return self._bytes

    @property
    def str(self) -> SnapshotString:
        if self._str is None:
            self._str = SnapshotString(self._update_snapshot)
        return self._str

    def __call__(self, data_to_snapshot: object, name: str = "", filetype="txt") -> None:
        if isinstance(data_to_snapshot, bytes):
            self.bytes(data_to_snapshot, name, filetype)
        elif isinstance(data_to_snapshot, str):
            self.str(data_to_snapshot, name, filetype)
        else:
            raise ValueError("Only bytes and strings are supported")
        
    def _save_test_results(self, path: pathlib.Path, data: object) -> None:
        if isinstance(data, bytes):
            self.bytes._save_test_results(path, data)
        elif isinstance(data, str):
            self.str._save_test_results(path, data)
        else:
            raise ValueError("Only bytes and strings are supported")
        
    def assert_match(self, value: object, file_name: str) -> None:
        if isinstance(value, bytes):
            self.bytes.assert_match(value, file_name)
        elif isinstance(value, str):
            self.str.assert_match(value, file_name)
        else:
            raise ValueError("Only bytes and strings are supported")