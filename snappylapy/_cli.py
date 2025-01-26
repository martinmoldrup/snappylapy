"""Create cli using the typer library."""
import re
import typer
import pathlib
from snappylapy.constants import directory_names

app = typer.Typer(
    no_args_is_help=True,
    help="""
    The CLI provides commands to initialize the repo and to clear test results and snapshots.
    In the future the future the CLI will be expanded with review and update commands.
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
    regex = re.compile(
        rf"^{re.escape(directory_names.test_results_dir_name)}(/|$)")
    if any(regex.match(line) for line in lines):
        typer.echo("Already in .gitignore.")
        return
    # Add to .gitignore to top of file
    line_to_add = f"# Ignore test results from snappylapy\n{directory_names.test_results_dir_name}/\n\n"
    with gitignore_path.open("w") as file:
        file.write(line_to_add)
        file.writelines(lines)
    typer.echo(
        f"Added {directory_names.test_results_dir_name}/ to .gitignore.")


@app.command()
def clear(force: bool = typer.Option(
    False,
    "--force",
    "-f",
    help="Force deletion without confirmation",
)) -> None:
    """Clear all test results and snapshots, recursively, using pathlib."""
    list_of_files_to_delete = get_files_to_delete()
    if not list_of_files_to_delete:
        typer.echo("No files to delete.")
        return
    if not force:
        # Ask for confirmation
        typer.secho(
            "\nAre you sure you want to delete all test results and snapshots?",
            fg=typer.colors.BRIGHT_BLUE)
        response = typer.prompt(
            "Type 'yes' to confirm, anything else to abort.")
        if response.lower() != "yes":
            typer.echo("Aborted.")
            return
    # Delete files
    delete_files(list_of_files_to_delete)
    typer.echo(f"Deleted {len(list_of_files_to_delete)} files.")


def get_files_to_delete() -> list[pathlib.Path]:
    """Get list of files to delete."""
    list_of_files_to_delete: list[pathlib.Path] = []
    for dir_name in [
            directory_names.test_results_dir_name,
            directory_names.snapshot_dir_name,
    ]:
        for root_dir in pathlib.Path().rglob(dir_name):
            for file in root_dir.iterdir():
                if file.is_file():
                    list_of_files_to_delete.append(file)
                    typer.echo(f"Found file to delete: {file}")
    return list_of_files_to_delete


def delete_files(list_of_files_to_delete: list[pathlib.Path]) -> None:
    """Delete files."""
    # Delete files
    for file in list_of_files_to_delete:
        file.unlink()
    # Delete directories
    for dir_name in [
            directory_names.test_results_dir_name,
            directory_names.snapshot_dir_name,
    ]:
        for root_dir in pathlib.Path().rglob(dir_name):
            root_dir.rmdir()


if __name__ == "__main__":
    app()
