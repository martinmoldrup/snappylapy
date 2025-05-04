"""Exceptions for SnappyLapy."""


class TestDirectoryNotParametrizedError(Exception):
    """Custom exception raised when the test_directory fixture is not parametrized."""

    def __init__(self) -> None:
        """Initialize the exception with a custom error message."""
        error_msg = (
            "The test_directory fixture is not parametrized, please add the snappylapy marker to the test, "
            "e.g. @pytest.mark.snappylapy(foreach_folder_in='test_data')"
        )
        super().__init__(error_msg)
