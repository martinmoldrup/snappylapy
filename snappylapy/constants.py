"""Read-only constants."""
import pathlib

DEFEAULT_SNAPSHOT_BASE_DIR = pathlib.Path()
OUTPUT_JSON_INDENTATION_LEVEL = 2

class DirectoryNames:
    """Class to enforce immutable directory names, since there is side effect if they are changed."""

    @property
    def snapshot_dir_name(self) -> str:
        """Snapshot directory name."""
        return "__snapshots__"

    @property
    def test_results_dir_name(self) -> str:
        """Test results directory name."""
        return "__test_results__"


directory_names = DirectoryNames()
