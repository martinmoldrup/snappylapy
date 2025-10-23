"""Models for snappylapy."""

from __future__ import annotations

import pathlib
from dataclasses import dataclass, field
from snappylapy.constants import DIRECTORY_NAMES


@dataclass
class DependingSettings:
    """Settings for depending on other snapshots. Used for loading snapshots."""

    test_filename: str
    """Filename of the test module where the depending test are defined."""

    test_function: str
    """Name of the depending test function."""

    snapshots_base_dir: pathlib.Path
    """Input base directory for loading snapshots."""

    filename_extension: str | None = None
    """Extension of the depending snapshot file."""

    custom_name: str | None = None
    """Custom name for the depending snapshot file."""

    @property
    def filename(self) -> str:
        """Get the depending snapshot filename."""
        if not self.filename_extension:
            msg = "Missing depending snapshot filename extension."
            raise ValueError(msg)
        if self.custom_name is not None:
            return f"[{self.test_filename}][{self.test_function}][{self.custom_name}].{self.filename_extension}"
        return f"[{self.test_filename}][{self.test_function}].{self.filename_extension}"


@dataclass
class Settings:
    """Shared setting for all the strategies for doing snapshot testing."""

    test_filename: str
    """Filename of the test module where the current test are defined."""

    test_function: str
    """Name of the test function."""

    custom_name: str | None = None
    """Custom name for the snapshot file."""

    snapshots_base_dir: pathlib.Path = pathlib.Path()
    """Output base directory for storing snapshots."""

    snapshot_update: bool = False
    """Flag to update the snapshots."""

    filename_extension: str = "txt"
    """Extension for the output of snapshot file."""

    # Configurations for depending
    depending_tests: list[DependingSettings] = field(default_factory=list)
    """
    Depending tests are used for loading snapshots from other tests.

    Information about each test the users have specified in a test decorator will be stored here.
    """

    @property
    def snapshot_dir(self) -> pathlib.Path:
        """Get the snapshot directory."""
        return pathlib.Path(self.snapshots_base_dir) / DIRECTORY_NAMES.snapshot_dir_name

    @property
    def test_results_dir(self) -> pathlib.Path:
        """Get the test results directory."""
        return pathlib.Path(self.snapshots_base_dir) / DIRECTORY_NAMES.test_results_dir_name

    @property
    def filename(self) -> str:
        """Get the snapshot filename."""
        if self.custom_name is not None:
            return f"[{self.test_filename}][{self.test_function}][{self.custom_name}].{self.filename_extension}"
        return f"[{self.test_filename}][{self.test_function}].{self.filename_extension}"
