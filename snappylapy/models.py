"""Models for snappylapy."""
import pathlib
from .constants import SNAPSHOT_DIR_NAME, TEST_RESULTS_DIR_NAME
from dataclasses import dataclass


@dataclass
class Settings:
    """Shared setting for all the strategies for doing snapshot testing."""

    snapshot_dir: pathlib.Path = pathlib.Path(SNAPSHOT_DIR_NAME)
    test_results_dir: pathlib.Path = pathlib.Path(TEST_RESULTS_DIR_NAME)
    snapshot_update: bool = False
    filename_base: str = "no_filename"
    filename_extension: str = "txt"

    @property
    def filename(self) -> str:
        """Get the snapshot filename."""
        return f"{self.filename_base}.{self.filename_extension}"
