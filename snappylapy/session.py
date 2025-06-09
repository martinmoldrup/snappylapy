"""Session for snapshot testing."""
import pathlib
from _pytest.terminal import TerminalReporter
from dataclasses import dataclass
from snappylapy.constants import DIRECTORY_NAMES


@dataclass
class SnapshotSession:
    """Session for snapshot testing."""

    def __init__(self) -> None:
        """Initialize the snapshot session."""
        self.snapshots_created: list[str] = []
        self.snapshots_updated: list[str] = []
        self.snapshot_tests_succeeded: list[str] = []
        self.snapshot_tests_failed: list[str] = []

    def _get_all_snapshots(self) -> set[str]:
        """Loop through all SNAPSHOT_DIR_NAME directories and return names of all snapshots."""
        snapshot_file_names: set[str] = set()
        # Find all directories called SNAPSHOT_DIR_NAME
        snapshot_dirs = list(pathlib.Path().rglob(
            DIRECTORY_NAMES.snapshot_dir_name))
        for snapshot_dir in snapshot_dirs:
            snapshot_file_names.update(
                snapshot_file.name for snapshot_file in snapshot_dir.iterdir())
        return snapshot_file_names

    def _get_unvisited_snapshots(self) -> set[str]:
        """Get all missing snapshots."""
        all_snapshots = self._get_all_snapshots()
        unvisited_snapshots = all_snapshots - set(
            self.snapshots_created + self.snapshots_updated +
            self.snapshot_tests_succeeded + self.snapshot_tests_failed)
        return unvisited_snapshots

    def on_finish(self) -> None:
        """On finish of the snapshot testing."""

    def has_ran_snapshot_tests(self) -> bool:
        """Check if snapshot tests have been run."""
        return bool(
            self.snapshots_created or self.snapshots_updated
            or self.snapshot_tests_succeeded)

    def write_summary(self, reporter: TerminalReporter) -> None:
        """Write the snapshot tests summary."""
        if not self.has_ran_snapshot_tests():
            return
        reporter.write_sep("=", "Snapshot tests summary", blue=True)
        if self.snapshot_tests_succeeded:
            reporter.write(
                f"Got {len(self.snapshot_tests_succeeded)} snapshot tests passing\n",
                green=True,
            )
        if self.snapshot_tests_failed:
            reporter.write(
                f"Got {len(self.snapshot_tests_failed)} snapshot tests failing\n",
                red=True,
            )
        if self.snapshots_updated:
            reporter.write("Updated snapshots:\n", green=True)
            for snapshot in self.snapshots_updated:
                reporter.write(f"  {snapshot}\n", blue=True)
        if self.snapshots_created:
            reporter.write("Created snapshots:\n", green=True)
            for snapshot in self.snapshots_created:
                reporter.write(f"  {snapshot}\n", blue=True)

        unvisited_snapshots = self._get_unvisited_snapshots()
        if unvisited_snapshots:
            reporter.write(
                f"Found {len(unvisited_snapshots)} unvisited snapshots:\n",
                red=True)
            for snapshot in unvisited_snapshots:
                reporter.write(f"  {snapshot}\n", blue=True)

    def add_created_snapshot(self, item: str) -> None:
        """Add a created snapshot."""
        self.snapshots_created.append(item)

    def add_updated_snapshot(self, item: str) -> None:
        """Add an updated snapshot."""
        self.snapshots_updated.append(item)

    def add_snapshot_test_succeeded(self, item: str) -> None:
        """Add a snapshot test that succeeded."""
        self.snapshot_tests_succeeded.append(item)

    def add_snapshot_test_failed(self, item: str) -> None:
        """Add a snapshot test that failed."""
        self.snapshot_tests_failed.append(item)
