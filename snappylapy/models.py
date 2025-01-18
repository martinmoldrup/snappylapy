"""Models for snappylapy."""
from __future__ import annotations

import pathlib
from dataclasses import dataclass
from snappylapy.constants import directory_names


@dataclass
class Settings:
    """Shared setting for all the strategies for doing snapshot testing."""

    test_filename: str
    """Filename of the test module where the test are defined."""

    test_function: str
    """Name of the test function."""

    custom_name: str | None = None
    """Custom name for the snapshot file."""

    snapshots_base_dir: str | pathlib.Path = pathlib.Path()
    snapshot_update: bool = False
    filename_extension: str = "txt"

    @property
    def snapshot_dir(self) -> pathlib.Path:
        """Get the snapshot directory."""
        return pathlib.Path(self.snapshots_base_dir) / directory_names.snapshot_dir_name

    @property
    def test_results_dir(self) -> pathlib.Path:
        """Get the test results directory."""
        return pathlib.Path(self.snapshots_base_dir) / directory_names.test_results_dir_name

    @property
    def filename(self) -> str:
        """Get the snapshot filename."""
        if self.custom_name:
            return f"[{self.test_filename}][{self.test_function}][{self.custom_name}].{self.filename_extension}"
        return f"[{self.test_filename}][{self.test_function}].{self.filename_extension}"
