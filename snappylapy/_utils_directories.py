"""Utility functions for handling directories in snappylapy."""
import pathlib
from snappylapy.constants import DIRECTORY_NAMES


def find_directories(directory_names: list[str]) -> list[pathlib.Path]:
    """Find directories with the given names."""
    found_dirs: list[pathlib.Path] = []
    for dir_name in directory_names:
        found_dirs.extend(pathlib.Path().rglob(dir_name))
    return found_dirs


def get_file_paths_from_directories(list_of_directories: list[pathlib.Path]) -> list[pathlib.Path]:
    """Get file paths from directories."""
    list_of_files_to_delete: list[pathlib.Path] = []
    for directory in list_of_directories:
        if not directory.is_dir():
            error_msg = f"{directory} is not a directory."
            raise ValueError(error_msg)
        list_of_files_to_delete.extend(file for file in directory.iterdir() if file.is_file())
    return list_of_files_to_delete


class DirectoryNamesUtil:
    """
    Utility class to handle directory names and operations related to them.

    This class extends the DirectoryNames class to provide methods for finding directories
    and file paths created by snappylapy.
    """

    def get_all_directory_names(self) -> list[str]:
        """Get all directory names."""
        return [DIRECTORY_NAMES.snapshot_dir_name, DIRECTORY_NAMES.test_results_dir_name]

    def get_all_directories_for_test_results(self) -> list[pathlib.Path]:
        """Get all directories for test results."""
        return find_directories([DIRECTORY_NAMES.test_results_dir_name])

    def get_all_directories_for_snapshots(self) -> list[pathlib.Path]:
        """Get all directories for snapshots."""
        return find_directories([DIRECTORY_NAMES.snapshot_dir_name])

    def get_all_file_paths_test_results(self) -> list[pathlib.Path]:
        """Get all file paths in the test results directory."""
        directories = find_directories([DIRECTORY_NAMES.test_results_dir_name])
        return get_file_paths_from_directories(directories)

    def get_all_file_paths_snapshots(self) -> list[pathlib.Path]:
        """Get all file paths in the snapshot directory."""
        directories = find_directories([DIRECTORY_NAMES.snapshot_dir_name])
        return get_file_paths_from_directories(directories)

    def get_all_directories_created_by_snappylapy(self) -> list[pathlib.Path]:
        """Get all directories created by snappylapy."""
        return find_directories(self.get_all_directory_names())

    def get_all_file_paths_created_by_snappylapy(self) -> list[pathlib.Path]:
        """Get all file paths created by snappylapy."""
        return get_file_paths_from_directories(
            self.get_all_directories_created_by_snappylapy(),
        )
