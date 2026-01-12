"""Create cli using the typer library."""

import re
import typer
import pathlib
import subprocess  # noqa: S404
from enum import Enum
from snappylapy._utils_directories import DirectoryNamesUtil
from snappylapy.constants import DIRECTORY_NAMES

app = typer.Typer(
    no_args_is_help=True,
    help="""
    Welcome to the snappylapy CLI!

    Use these commands to initialize your repository, update or clear test results and snapshots,
    and review differences between your test results and snapshots using the 'diff' command.

    - Run *'init'* to set up your repo for snappylapy.
    - Use *'status'* to see the current status of your snapshots.
    - Use *'update'* to refresh snapshots with the latest test results.
    - Use *'clear'* to remove all test results and snapshots (add --force to skip confirmation).
    - Use *'diff'* to view changes between test results and snapshots in your editor.

    For more details on each command, use --help after the command name.
    """,
)


@app.command()
def init() -> None:
    """
    Run this command to initialize your repository for snappylapy.

    This will add a line to your .gitignore file to ensure test results are not tracked by git.
    """
    # Check if .gitignore exists
    gitignore_path = pathlib.Path(".gitignore")
    if not gitignore_path.exists():
        typer.echo("No .gitignore file found. Creating one.")
        gitignore_path.touch()
    # Check if already in .gitignore
    with gitignore_path.open("r") as file:
        lines = file.readlines()
    regex = re.compile(rf"^{re.escape(DIRECTORY_NAMES.test_results_dir_name)}(/|$)")
    if any(regex.match(line) for line in lines):
        typer.echo("Already in .gitignore.")
        return
    # Add to .gitignore to top of file
    line_to_add = f"# Ignore test results from snappylapy\n{DIRECTORY_NAMES.test_results_dir_name}/\n\n"
    with gitignore_path.open("w") as file:
        file.write(line_to_add)
        file.writelines(lines)
    typer.echo(f"Added {DIRECTORY_NAMES.test_results_dir_name}/ to .gitignore.")


@app.command()
def status() -> None:
    """
    Show the status of all files in the snapshot directory.

    This will list how many files are unchanged, changed, or not found compared to the snapshots.
    """
    status_fetcher = _SnapshotStatusManager()
    status_fetcher.print_status()


@app.command()
def clear(
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force deletion without confirmation",
    ),
) -> None:
    """
    Use this command to clear all test results and snapshots created by snappylapy.

    This will recursively delete all files and directories related to test results and snapshots.
    Use --force to skip confirmation.

    This finds and deletes all `__test_results__` and `__snapshots__` directories recursively across the working directory.
    """  # noqa: E501
    list_of_files_to_delete = DirectoryNamesUtil().all_file_paths_created_by_snappylapy
    if not list_of_files_to_delete:
        typer.echo("No files to delete.")
        return
    _print_deletion_summary(
        directories_to_delete=DirectoryNamesUtil().all_directories_created_by_snappylapy,
        list_of_files_to_delete=list_of_files_to_delete,
    )
    if not force and not _user_approved_deletion_in_cli():
        return
    # Delete files
    _delete_files(list_of_files_to_delete)
    typer.echo(f"Deleted {len(list_of_files_to_delete)} files.")


@app.command()
def update() -> None:
    """
    Use this command to update all snapshot files with the latest test results.

    This will overwrite existing snapshots with current test outputs, ensuring your snapshots reflect the latest changes.

    The file contents of any files in any of the `__test_results__` folders will be copied to the corresponding `__snapshots__` folder.
    """  # noqa: E501
    status_fetcher = _SnapshotStatusManager()
    if status_fetcher.get_count_of_test_results_files() == 0:
        typer.echo("No test result files found. Run pytest tests that use snappylapy expectations first.")
        return
    files_to_update = status_fetcher.get_files_to_be_updated()
    count_up_to_date_files = status_fetcher.get_count_of_test_results_files() - len(files_to_update)
    if not files_to_update:
        typer.echo(f"All snapshot files are up to date. {count_up_to_date_files} files are up to date.")
        return

    typer.echo(
        f"Found {len(files_to_update)} files to update."
        + (f" {count_up_to_date_files} files are up to date." if count_up_to_date_files > 0 else ""),
    )
    for test_result_file_path in files_to_update:
        snapshot_file_path = _get_snapshot_path_from_test_result_path(test_result_file_path)
        snapshot_file_path.parent.mkdir(parents=True, exist_ok=True)
        snapshot_file_path.write_bytes(test_result_file_path.read_bytes())
        typer.echo(f"Updated snapshot: {snapshot_file_path}")

    typer.echo("Finished updating snapshots.")


@app.command()
def diff() -> None:
    """
    Show the differences between the test results and the snapshots.

    Opens all of the changed diffs in the Visual Studio Code (VSCode) editor.
    This requires that you have VSCode installed and the `code` command available in your PATH.

    More diff viewers will be supported in the future, please raise a request on github with your needs.
    """
    status_fetcher = _SnapshotStatusManager()
    files_to_diff = status_fetcher.get_files_with_status(FileStatus.CHANGED)
    if not files_to_diff:
        status_fetcher.print_status()
        typer.echo("No files have changed, not opening any diffs.")
        return
    typer.echo(f"Opening diffs for {len(files_to_diff)} changed files.")
    for test_result_file_path in files_to_diff:
        open_diff_viewer(
            test_result_file_path=test_result_file_path,
            snapshot_file_path=_get_snapshot_path_from_test_result_path(test_result_file_path),
        )


def _get_snapshot_path_from_test_result_path(test_result_file_path: pathlib.Path) -> pathlib.Path:
    """Get the snapshot file path from the test result file path."""
    return test_result_file_path.parent.parent / DIRECTORY_NAMES.snapshot_dir_name / test_result_file_path.name


def open_diff_viewer(test_result_file_path: pathlib.Path, snapshot_file_path: pathlib.Path) -> None:
    """Open diff viewer for the given file."""
    success: bool = _try_open_diff(test_result_file_path, snapshot_file_path)
    if not success:
        typer.secho(
            f"Could not open diff tool. Files to compare:\n"
            f"  Test result: {test_result_file_path.resolve()}\n"
            f"  Snapshot:    {snapshot_file_path.resolve()}",
            fg=typer.colors.YELLOW,
        )


class FileStatus(Enum):
    """Enum to represent the status of a file."""

    NOT_FOUND = "not_found"
    CHANGED = "changed"
    UNCHANGED = "unchanged"


def _user_approved_deletion_in_cli() -> bool:
    """Ask user for confirmation before deleting files."""
    typer.secho("\nAre you sure you want to delete all test results and snapshots?", fg=typer.colors.BRIGHT_BLUE)
    response = typer.prompt("Type 'yes' to confirm, anything else to abort.", default="no")
    if response.lower() == "yes":
        typer.echo("User confirmed, deleting files.")
        return True
    typer.echo("Aborted, not deleting any files.")
    return False


def _print_deletion_summary(
    directories_to_delete: list[pathlib.Path],
    list_of_files_to_delete: list[pathlib.Path],
) -> None:
    """Print summary of files and directories to be deleted."""
    typer.echo("Deleting files:")
    for file in list_of_files_to_delete:
        typer.echo(f"- {file}")

    typer.secho(
        f"Deleting {len(list_of_files_to_delete)} files from {len(directories_to_delete)} directories:",
        fg=typer.colors.BRIGHT_BLUE,
    )
    for directory in directories_to_delete:
        typer.echo(f"- {directory}")


def _delete_files(list_of_files_to_delete: list[pathlib.Path]) -> None:
    """Delete files."""
    # Delete files
    for file in list_of_files_to_delete:
        file.unlink()
    # Delete directories
    for dir_name in [
        DIRECTORY_NAMES.test_results_dir_name,
        DIRECTORY_NAMES.snapshot_dir_name,
    ]:
        for root_dir in pathlib.Path().rglob(dir_name):
            root_dir.rmdir()


def _try_open_diff(file1: pathlib.Path, file2: pathlib.Path) -> bool:
    """Try to open diff using available tools, return True if successful."""
    diff_commands: list[list[str]] = [
        ["code", "--diff", str(file1.resolve()), str(file2.resolve())],
        ["code.cmd", "--diff", str(file1.resolve()), str(file2.resolve())],  # Windows alternative
    ]

    for command in diff_commands:
        try:
            subprocess.run(command, check=True, timeout=10)  # noqa: S603 - shell=False and args as list, safe usage
        except subprocess.TimeoutExpired:  # noqa: PERF203
            typer.secho(
                f"Diff tool timed out for command: {' '.join(command)}",
                fg=typer.colors.RED,
            )
            continue
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
        else:
            return True
    return False


class _SnapshotStatusManager:
    """Various utilities to get various snapshot statuses and information."""

    def _check_file_statuses(
        self,
    ) -> dict[pathlib.Path, FileStatus]:
        """Check the status of files in the snapshot directory."""
        files_test_results = DirectoryNamesUtil().all_file_paths_test_results
        file_statuses: dict[pathlib.Path, FileStatus] = {}
        for file_path in files_test_results:
            snapshot_file = file_path.parent.parent / DIRECTORY_NAMES.snapshot_dir_name / file_path.name
            if not snapshot_file.exists():
                file_statuses[file_path] = FileStatus.NOT_FOUND
            elif snapshot_file.stat().st_size != file_path.stat().st_size:
                # TODO: This is not foolproof, does not catch content swaps and byte flips.
                file_statuses[file_path] = FileStatus.CHANGED
            elif snapshot_file.read_bytes() != file_path.read_bytes():
                # TODO: Expensive call, store hashes instead in a data file.
                file_statuses[file_path] = FileStatus.CHANGED
            else:
                file_statuses[file_path] = FileStatus.UNCHANGED
        return file_statuses

    def get_count_of_test_results_files(self) -> int:
        """Return the count of all test results files."""
        files_test_results = DirectoryNamesUtil().all_file_paths_test_results
        return len(files_test_results)

    def _get_status_counts(self) -> dict[FileStatus, int]:
        """Return a dict with counts of each file status for snapshot files."""
        file_statuses: dict[pathlib.Path, FileStatus] = self._check_file_statuses()
        status_counts: dict[FileStatus, int] = dict.fromkeys(FileStatus, 0)
        for status in file_statuses.values():
            status_counts[status] += 1
        return status_counts

    def get_files_with_status(
        self,
        status: FileStatus,
    ) -> list[pathlib.Path]:
        """Get all files with the desired status."""
        file_statuses: dict[pathlib.Path, FileStatus] = self._check_file_statuses()
        return [file for file, file_status in file_statuses.items() if file_status == status]

    def get_files_to_be_updated(self) -> list[pathlib.Path]:
        """Get all files that need to be updated (not unchanged)."""
        file_statuses: dict[pathlib.Path, FileStatus] = self._check_file_statuses()
        return [file for file, file_status in file_statuses.items() if file_status != FileStatus.UNCHANGED]

    def print_status(self) -> None:
        """Print the current status of the snapshot files to the console."""
        status_counts = self._get_status_counts()
        if not status_counts or sum(status_counts.values()) == 0:
            typer.secho("No test result files found.", fg=typer.colors.YELLOW)
            return

        typer.secho("Snapshot status:", underline=True, bold=True)
        for status in FileStatus:
            typer.echo(f"- {status.value}: {status_counts[status]} file(s)")

        if status_counts[FileStatus.CHANGED] > 0 or status_counts[FileStatus.NOT_FOUND] > 0:
            typer.secho("Some files are changed or missing snapshots.", fg=typer.colors.RED)
        else:
            typer.secho("All files are up to date.", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
