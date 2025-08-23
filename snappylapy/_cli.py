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
    The CLI provides commands to initialize the repo and to update or clear test results and snapshots.
    In the future the future the CLI will be expanded with review.
    """,
)


@app.command()
def init() -> None:
    """Initialize repo by adding line to .gitignore."""
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
def clear(
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force deletion without confirmation",
    ),
) -> None:
    """Clear all test results and snapshots, recursively, using pathlib."""
    directories_to_delete = DirectoryNamesUtil().get_all_directories_created_by_snappylapy()
    list_of_files_to_delete = DirectoryNamesUtil().get_all_file_paths_created_by_snappylapy()
    if not list_of_files_to_delete:
        typer.echo("No files to delete.")
        return
    if not force:
        typer.echo("Deleting files:")
        for file in list_of_files_to_delete:
            typer.echo(f"- {file}")

        typer.secho(
            f"Deleting {len(list_of_files_to_delete)} files from {len(directories_to_delete)} directories:",
            fg=typer.colors.BRIGHT_BLUE,
        )
        for directory in directories_to_delete:
            typer.echo(f"- {directory}")

        # Ask for confirmation
        typer.secho("\nAre you sure you want to delete all test results and snapshots?", fg=typer.colors.BRIGHT_BLUE)
        response = typer.prompt("Type 'yes' to confirm, anything else to abort.", default="no")
        if response.lower() != "yes":
            typer.echo("Aborted.")
            return
    # Delete files
    delete_files(list_of_files_to_delete)
    typer.echo(f"Deleted {len(list_of_files_to_delete)} files.")


@app.command()
def update() -> None:
    """Update the snapshot files by copying the test results, to the snapshot directory."""
    files_test_results = DirectoryNamesUtil().get_all_file_paths_test_results()
    if not files_test_results:
        typer.echo("No files to update.")
        return
    file_statuses = check_file_statuses(files_test_results)
    files_to_update = [file for file, status in file_statuses.items() if status != FileStatus.UNCHANGED]
    count_up_to_date_files = len(files_test_results) - len(files_to_update)
    if not files_to_update:
        typer.echo(f"All snapshot files are up to date. {count_up_to_date_files} files are up to date.")
        return

    typer.echo(
        f"Found {len(files_to_update)} files to update."
        + (f" {count_up_to_date_files} files are up to date." if count_up_to_date_files > 0 else ""),
    )
    for file in files_to_update:
        snapshot_file = file.parent.parent / DIRECTORY_NAMES.snapshot_dir_name / file.name
        snapshot_file.parent.mkdir(parents=True, exist_ok=True)
        snapshot_file.write_bytes(file.read_bytes())
        typer.echo(f"Updated snapshot: {snapshot_file}")


@app.command()
def diff() -> None:
    """Show the differences between the test results and the snapshots."""
    files_test_results = DirectoryNamesUtil().get_all_file_paths_test_results()
    file_statuses = check_file_statuses(files_test_results)
    files_to_diff = [file for file, status in file_statuses.items() if status == FileStatus.CHANGED]
    if not files_to_diff:
        status_counts: dict[FileStatus, int] = dict.fromkeys(FileStatus, 0)
        for status in file_statuses.values():
            status_counts[status] += 1

        typer.secho("File status counts:", underline=True, bold=True)
        for status, count in status_counts.items():
            typer.echo(f"- {status.value}: {count} file(s)")
        typer.echo("No files have changed, not opening any diffs.")
        return
    typer.echo(f"Opening diffs for {len(files_to_diff)} changed files.")
    for file in files_to_diff:
        snapshot_file = file.parent.parent / DIRECTORY_NAMES.snapshot_dir_name / file.name
        success: bool = _try_open_diff(file, snapshot_file)
        if not success:
            typer.secho(
                f"Could not open diff tool. Files to compare:\n"
                f"  Test result: {file.resolve()}\n"
                f"  Snapshot:    {snapshot_file.resolve()}",
                fg=typer.colors.YELLOW,
            )


def delete_files(list_of_files_to_delete: list[pathlib.Path]) -> None:
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


class FileStatus(Enum):
    """Enum to represent the status of a file."""

    NOT_FOUND = "not_found"
    CHANGED = "changed"
    UNCHANGED = "unchanged"


def check_file_statuses(
    file_paths: list[pathlib.Path],
) -> dict[pathlib.Path, FileStatus]:
    """Check the status of files in the snapshot directory."""
    file_statuses: dict[pathlib.Path, FileStatus] = {}
    for file_path in file_paths:
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


if __name__ == "__main__":
    app()
