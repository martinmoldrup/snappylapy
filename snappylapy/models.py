"""Models for snappylapy."""
from __future__ import annotations

import pathlib
from .constants import SNAPSHOT_DIR_NAME, TEST_RESULTS_DIR_NAME
from dataclasses import dataclass


@dataclass
class Settings:
    """Shared setting for all the strategies for doing snapshot testing."""

    test_filename: str
    """Filename of the test module where the test are defined."""

    test_function: str
    """Name of the test function."""

    custom_name: str | None = None
    """Custom name for the snapshot file."""

    snapshot_dir: pathlib.Path = pathlib.Path(SNAPSHOT_DIR_NAME)
    test_results_dir: pathlib.Path = pathlib.Path(TEST_RESULTS_DIR_NAME)
    snapshot_update: bool = False
    filename_extension: str = "txt"

    @property
    def filename(self) -> str:
        """Get the snapshot filename."""
        if self.custom_name:
            return f"[{self.test_filename}][{self.test_function}][{self.custom_name}].{self.filename_extension}"
        return f"[{self.test_filename}][{self.test_function}].{self.filename_extension}"
