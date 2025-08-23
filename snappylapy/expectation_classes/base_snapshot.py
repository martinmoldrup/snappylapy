"""Base class for snapshot testing."""
from __future__ import annotations

import pathlib
from abc import ABC, abstractmethod
from snappylapy.models import Settings
from snappylapy.serialization import Serializer
from snappylapy.session import SnapshotSession
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseSnapshot(ABC, Generic[T]):
    """Base class for snapshot testing."""

    serializer_class: type[Serializer[T]]

    def __init__(
        self,
        settings: Settings,
        snappylapy_session: SnapshotSession,
    ) -> None:
        """Initialize the base snapshot."""
        self.settings = settings
        self._data: T | None = None
        self.snappylapy_session = snappylapy_session

    @abstractmethod
    def __call__(
        self,
        data_to_snapshot: T,
        name: str | None = None,
        filetype: str = "snapshot.txt",
    ) -> BaseSnapshot[T]:
        """Prepare data for snapshot testing."""

    def to_match_snapshot(self) -> None:
        """Assert test results match the snapshot."""
        if not (self.settings.snapshot_dir / self.settings.filename).exists():
            if not self.settings.snapshot_update:
                error_msg = f"Snapshot file not found: {self.settings.filename}, run 'snappylapy update' command in the terminal, or run pytest with the --snapshot-update flag to create it."  # noqa: E501
                raise FileNotFoundError(error_msg)
            self.snappylapy_session.add_created_snapshot(
                self.settings.filename)
            self._update_snapshot()
            return

        snapshot_data = self._read_file(self.settings.snapshot_dir /
                                        self.settings.filename)
        test_data = self._read_file(self.settings.test_results_dir /
                                    self.settings.filename)
        try:
            snapshot_data_str = snapshot_data.decode()
            snapshot_data_str = snapshot_data_str.replace("\r\n", "\n").replace("\r", "\n")
            test_data_str = test_data.decode()
            test_data_str = test_data_str.replace("\r\n", "\n").replace("\r", "\n")
            assert snapshot_data_str == test_data_str
        except AssertionError as error:
            if self.settings.snapshot_update:
                self.snappylapy_session.add_updated_snapshot(
                    self.settings.filename)
                self._update_snapshot()
            else:
                self.snappylapy_session.add_snapshot_test_failed(
                    self.settings.filename)
                diff_msg = str(error)
                error_msg = f"Snapshot does not match test results. Run pytest with the --snapshot-update flag to update the snapshot.\n{diff_msg}"  # noqa: E501
                raise AssertionError(error_msg)  # noqa: B904
        else:
            self.snappylapy_session.add_snapshot_test_succeeded(
                self.settings.filename)

    def _prepare_test(self, data: T, name: str | None, extension: str) -> None:
        """Prepare and save test results."""
        if name is not None:
            self.settings.custom_name = str(name)
        self._data = data
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

    def _save_test_results(self, path: pathlib.Path, data: T) -> None:
        """Save data for test results."""
        data_bin = self.serializer_class().serialize(data)
        path.write_bytes(data_bin)
