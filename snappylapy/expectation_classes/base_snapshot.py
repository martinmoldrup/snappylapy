"""Base class for snapshot testing."""
from __future__ import annotations

import inspect
import pathlib
from abc import ABC
from snappylapy.models import Settings
from snappylapy.serialization import Serializer
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseSnapshot(ABC, Generic[T]):
    """Base class for snapshot testing."""

    serializer_class: type[Serializer[T]]

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
        try:
            snapshot_data_str = snapshot_data.decode()
            test_data_str = test_data.decode()
            assert snapshot_data_str == test_data_str
        except AssertionError as error:
            diff_msg = str(error)
            error_msg = f"Snapshot does not match test results. Run pytest with the --snapshot-update flag to update the snapshot.\n{diff_msg}"  # noqa: E501
            raise AssertionError(error_msg)  # noqa: B904

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
        parent_module_path = pathlib.Path(__file__).parent
        while frame:
            file_path_of_frame = pathlib.Path(frame.f_code.co_filename)
            if parent_module_path not in file_path_of_frame.parents:
                return frame.f_code.co_name
            frame = frame.f_back
        error_msg = "Could not derive filename from stack."
        raise ValueError(error_msg)

    def _save_test_results(self, path: pathlib.Path, data: T) -> None:
        """Save data for test results."""
        data_bin = self.serializer_class().serialize(data)
        path.write_bytes(data_bin)
