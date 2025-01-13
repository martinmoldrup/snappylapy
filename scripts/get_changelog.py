"""Python script for getting the change log entry from the CHANGELOG.md file."""
import pathlib
import argparse

PATH = pathlib.Path(__file__).parent.parent / "CHANGELOG.md"

parser = argparse.ArgumentParser(description="Get the change log entry for a version.")
parser.add_argument("version", help="The version to get the change log entry for.")
args = parser.parse_args()

version = args.version
if not version:
    raise ValueError("No version provided.")


with PATH.open("r", encoding="utf-8") as file:
    lines = file.readlines()

version_str = f"## [{version}]"
version_str_next = f"## ["
change_log = []
found = False
for line in lines:
    if found:
        if line.startswith(version_str_next):
            break
        change_log.append(line)
    if line.startswith(version_str):
        found = True

if not change_log:
    raise ValueError(f"Version {version} not found in change log.")

print("".join(change_log))
