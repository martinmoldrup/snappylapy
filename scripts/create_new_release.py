"""Create a new release for the project, by reading the version from the pyproject.toml file, and adding and pushing a new tag to the repository."""
import os
import subprocess
import toml
import pathlib
import requests
from packaging.version import Version

PYPROJECT_TOML = pathlib.Path(__file__).parent.parent / "pyproject.toml"
CHANGELOG_MD = pathlib.Path(__file__).parent.parent / "CHANGELOG.md"
PYPI_ENDPOINT = "https://pypi.org/pypi/snappylapy/json"

def read_version():
    """Read the version from the pyproject.toml file."""
    with open(PYPROJECT_TOML, "r", encoding="utf-8") as file:
        data = toml.load(file)
    return data["project"]["version"]

def check_version(version: str):
    """Check if the version is newer than the one in pypi."""
    response = requests.get(PYPI_ENDPOINT)
    pypi_version = response.json()["info"]["version"]
    print(f"Version in pypi: {pypi_version}")
    if Version(version) <= Version(pypi_version):
        raise ValueError(f"Version {version} is not newer than the one in pypi: {pypi_version}")
    
def check_change_log(version: str):
    """Check if the version has a corresponding entry in the change log. It will be a line starting with ## [0.0.2]"""
    with open(CHANGELOG_MD, "r", encoding="utf-8") as file:
        lines = file.readlines()
    version_str = f"## [{version}]"
    if not any(line.startswith(version_str) for line in lines):
        raise ValueError(f"Version {version} does not have a corresponding entry in the change log.")
    print(f"Version {version} has a corresponding entry in the change log.")



if __name__ == "__main__":
    version = read_version()
    print(f"Creating a new release for version {version}.")
    check_version(version)
    check_change_log(version)

    # Get confirmation from the user
    response = input("Do you want to continue? (yes/no) or (y/n): ")
    if response.lower() != "yes" and response.lower() != "y":
        print("Release creation aborted.")
        os._exit(1)

    # # Create a new tag
    res = subprocess.run(["git", "tag", version])
    if res.returncode != 0:
        raise ValueError(f"Error creating tag {version}")

    # Push the new tag
    res = subprocess.run(["git", "push", "origin", version])
    if res.returncode != 0:
        raise ValueError(f"Error pushing tag {version}")

    print("Release created successfully.")