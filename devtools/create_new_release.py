"""Create a new release for the project, by reading the version from the pyproject.toml file, and adding and pushing a new tag to the repository."""
import sys
import toml
import typer
import pathlib
import requests
import subprocess
from packaging.version import Version
from toolit import tool

PYPROJECT_TOML = pathlib.Path(__file__).parent.parent / "pyproject.toml"
CHANGELOG_MD = pathlib.Path(__file__).parent.parent / "CHANGELOG.md"
PYPI_ENDPOINT = "https://pypi.org/pypi/snappylapy/json"

def read_pyproject_version() -> Version:
    """Read the version from the pyproject.toml file."""
    with open(PYPROJECT_TOML, "r", encoding="utf-8") as file:
        data = toml.load(file)
    version_str = data["project"]["version"]
    return Version(version_str)

def read_pypi_version() -> Version:
    """Check if the version is newer than the one in pypi."""
    response = requests.get(PYPI_ENDPOINT)
    version_str = response.json()["info"]["version"]
    return  Version(version_str)

def check_change_log(version: Version) -> bool:
    """Check if the version has a corresponding entry in the change log. It will be a line starting with ## [0.0.2]"""
    with open(CHANGELOG_MD, "r", encoding="utf-8") as file:
        lines = file.readlines()
    version_str = f"## [{version}]"
    return any(line.startswith(version_str) for line in lines)


@tool
def create_new_release() -> None:
    """Create a new release for the project by reading the version from the pyproject.toml file, checking the change log, and pushing a new tag to the repository."""
    if not PYPROJECT_TOML.exists():
        raise FileNotFoundError(f"{PYPROJECT_TOML} does not exist. Please run this script from the project root directory, and ensure the {PYPROJECT_TOML} file exists.")
    if not CHANGELOG_MD.exists():
        raise FileNotFoundError(f"{CHANGELOG_MD} does not exist. Please run this script from the project root directory, and ensure the {CHANGELOG_MD} file exists.")
    version_pyproject: Version = validate_and_get_version()
    validate_change_log_entry(version_pyproject)
    response: str = typer.prompt(
        f"Do you want to create a new release for version {typer.style(str(version_pyproject), fg=typer.colors.GREEN, bold=True)}? "
        "This will create a new tag and push it to the repository. (yes/no)",
        default="no",
    )
    if response.lower() not in ("yes", "y"):
        typer.secho("Release creation aborted.", fg=typer.colors.RED, bold=True)

        sys.exit(1)

    # Create a new tag
    res: subprocess.CompletedProcess = subprocess.run(["git", "tag", str(version_pyproject)])
    if res.returncode != 0:
        raise ValueError(f"Error creating tag {version_pyproject}")

    # Push the new tag
    res = subprocess.run(["git", "push", "origin", str(version_pyproject)])
    if res.returncode != 0:
        raise ValueError(f"Error pushing tag {version_pyproject}")

    typer.secho("Release created successfully.", fg=typer.colors.GREEN, bold=True)


def validate_and_get_version() -> Version:
    """Validate the version from the pyproject.toml file and check if it is newer than the one in pypi."""
    version_pyproject: Version = read_pyproject_version()
    typer.echo(f"Creating a new release for version {typer.style(str(version_pyproject), fg=typer.colors.GREEN, bold=True)} (read from {PYPROJECT_TOML}).")
    version_pypi: Version = read_pypi_version()
    typer.echo(
        f"Current version in pypi is {typer.style(str(version_pypi), fg=typer.colors.YELLOW, bold=True)} (read from {PYPI_ENDPOINT})."
    )
    typer.echo(
        f"Validating the "
        f"{typer.style(str(version_pypi), fg=typer.colors.YELLOW, bold=True)}"
        " -> "
        f"{typer.style(str(version_pyproject), fg=typer.colors.GREEN, bold=True)} deployment."
    )
    if version_pyproject <= version_pypi:
        error_message = (
            f"Version {version_pyproject} is not newer than the one in pypi. "
            "Please update the version in pyproject.toml."
        )
        raise ValueError(error_message)
    return version_pyproject

def validate_change_log_entry(version_pyproject: Version):
    """Validate that the version has a corresponding entry in the change log."""
    if not check_change_log(version_pyproject):
        error_message = (
            f"Version {version_pyproject} does not have a corresponding entry in the change log."
        )
        raise ValueError(error_message)
    typer.secho(
        f"Version {version_pyproject} has a corresponding entry in the change log.",
        fg=typer.colors.GREEN,
        bold=True,
    )

if __name__ == "__main__":
    create_new_release()