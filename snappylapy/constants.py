"""Read-only constants."""

import pathlib
from typing import NamedTuple

DEFAULT_SNAPSHOT_BASE_DIR = pathlib.Path()
OUTPUT_JSON_INDENTATION_LEVEL = 2


class DirectoryNames(NamedTuple):
    """Immutable directory names for snappylapy."""

    snapshot_dir_name: str
    test_results_dir_name: str


DIRECTORY_NAMES: DirectoryNames = DirectoryNames(
    snapshot_dir_name="__snapshots__", test_results_dir_name="__test_results__",
)
