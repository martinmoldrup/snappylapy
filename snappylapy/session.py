from dataclasses import dataclass
from _pytest.terminal import TerminalReporter
import pathlib
from snappylapy.constants import SNAPSHOT_DIR_NAME

@dataclass
class SnapshotSession:

    def __init__(self):
        self.snapshots_created: list[str] = []
        self.snapshots_updated: list[str] = []
        self.snapshot_tests_succeeded: list[str] = []
        self.snapshot_tests_failed: list[str] = []

    def _get_all_snapshots(self) -> set[str]:
        """Loop through all SNAPSHOT_DIR_NAME directories and return names of all snapshots."""
        snapshot_file_names: set[str] = set()
        # Find all directories called SNAPSHOT_DIR_NAME
        snapshot_dirs = list(pathlib.Path().rglob(SNAPSHOT_DIR_NAME))
        for snapshot_dir in snapshot_dirs:
            for snapshot_file in snapshot_dir.iterdir():
                snapshot_file_names.add(snapshot_file.name)
        return snapshot_file_names

    def _get_unvisited_snapshots(self) -> set[str]:
        """Get all missing snapshots."""
        all_snapshots = self._get_all_snapshots()
        unvisited_snapshots = all_snapshots - set(self.snapshots_created + self.snapshots_updated + self.snapshot_tests_succeeded + self.snapshot_tests_failed)
        return unvisited_snapshots

    def on_finish(self) -> None:
        """"""

    def has_ran_snapshot_tests(self) -> bool:
        return bool(
            self.snapshots_created or self.snapshots_updated
            or self.snapshot_tests_succeeded, )

    def write_summary(self, reporter: TerminalReporter) -> None:
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
            reporter.write(f"Found {len(unvisited_snapshots)} unvisited snapshots:\n", red=True)
            for snapshot in unvisited_snapshots:
                reporter.write(f"  {snapshot}\n", blue=True)

    def add_created_snapshot(self, item: str) -> None:
        self.snapshots_created.append(item)

    def add_updated_snapshot(self, item: str) -> None:
        self.snapshots_updated.append(item)

    def add_snapshot_test_succeeded(self, item: str) -> None:
        self.snapshot_tests_succeeded.append(item)

    def add_snapshot_test_failed(self, item: str) -> None:
        self.snapshot_tests_failed.append(item)
