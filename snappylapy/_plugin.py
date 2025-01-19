"""Pytest plugin for snapshot testing."""
import os
import pathlib
from typing import Any
import pytest
import _pytest.mark
from snappylapy import Expect, LoadSnapshot
from snappylapy.fixtures import Settings
from snappylapy.session import SnapshotSession
from snappylapy.constants import DEFEAULT_SNAPSHOT_BASE_DIR


def _get_kwargs_from_depend_function(depends_function, marker_name: str, kwags_key: str) -> Any:
    """Get a test function with a pytest marker assigned and get a value from the marker."""
    if not hasattr(depends_function, "pytestmark"):
        return None
    marks: list[_pytest.mark.structures.Mark] = depends_function.pytestmark
    for mark in marks:
        if mark.name == marker_name:
            return mark.kwargs.get(kwags_key, None)
    return None

def _get_args_from_depend_function(depends_function, marker_name: str) -> Any:
    """Get a test function with a pytest marker assigned and get a value from the marker."""
    if not hasattr(depends_function, "pytestmark"):
        return None
    marks: list[_pytest.mark.structures.Mark] = depends_function.pytestmark
    for mark in marks:
        if mark.name == marker_name:
            return mark.args
    return None

@pytest.fixture
def snappylapy_settings(request: pytest.FixtureRequest) -> Settings:
    """Initialize the Settings object for the test."""
    marker = request.node.get_closest_marker("snappylapy")
    settings = Settings(
        test_filename=request.module.__name__,
        test_function=request.node.name,
    )
    if marker:
        output_dir = marker.kwargs.get("output_dir", None)
        if output_dir:
            settings.snapshots_base_dir = output_dir
    if hasattr(request, 'param'):
        settings.snapshots_base_dir = request.param
    return settings


@pytest.fixture
def expect(request: pytest.FixtureRequest, snappylapy_settings: Settings) -> Expect:
    """Initialize the snapshot object with update_snapshots flag from pytest option."""
    update_snapshots = request.config.getoption("--snapshot-update")
    snappylapy_session: SnapshotSession = request.config.snappylapy_session  # type: ignore[attr-defined]
    return Expect(
        update_snapshots=update_snapshots,
        test_filename=snappylapy_settings.test_filename,
        test_function=snappylapy_settings.test_function,
        snappylapy_session=snappylapy_session,
        output_dir=snappylapy_settings.snapshots_base_dir,
    )


@pytest.fixture
def load_snapshot(request: pytest.FixtureRequest, snappylapy_settings: Settings) -> LoadSnapshot:
    """Initialize the LoadSnapshot object."""
    marker = request.node.get_closest_marker("snappylapy")
    depends = marker.kwargs.get("depends", []) if marker else []
    input_dir_from_depends = _get_kwargs_from_depend_function(depends[0], "snappylapy", "output_dir") if depends else None
    read_from_dir = pathlib.Path(input_dir_from_depends) if input_dir_from_depends else DEFEAULT_SNAPSHOT_BASE_DIR
    if not depends:
        return LoadSnapshot(snappylapy_settings, read_from_dir)

    snappylapy_settings.test_function = depends[0].__name__
    snappylapy_settings.test_filename = depends[0].__module__
    return LoadSnapshot(snappylapy_settings, read_from_dir)


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(
    session: pytest.Session,
    config: pytest.Config,
    items: list[pytest.Function],
) -> None:
    """Sort the tests based on the dependencies."""
    del config, session  # Unused
    for item in items:
        marker = item.get_closest_marker("snappylapy")
        if not marker:
            continue
        depends = marker.kwargs.get("depends", [])
        for depend in depends:
            for i, test in enumerate(items):
                if test.function != depend:
                    continue
                # Check if it is already earlier in the list than the dependency
                if i < items.index(item):
                    # Preserve the original order
                    break
                # Move the test to the position after the dependency
                items.insert(i + 1, items.pop(items.index(item)))
                break


def pytest_configure(config: pytest.Config) -> None:
    """Register the markers used."""
    config.addinivalue_line(
        "markers",
        "snappylapy: mark test to load snapshot data from a file.",
    )


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add the CLI option for updating snapshots."""
    group = parser.getgroup("terminal reporting")
    group.addoption(
        "--snapshot-update",
        action="store_true",
        dest="snapshot_update",
        default=False,
        help="update snapshots.",
    )


def pytest_sessionstart(session: pytest.Session) -> None:
    """Initialize the snapshot session."""
    session.config.snappylapy_session = SnapshotSession()  # type: ignore[attr-defined]


class ExceptionDuringTestSetupError(Exception):
    """Error raised when an exception is raised during the setup of the tests."""

class ReturnError():
    """When an exception is raised during the setup of the tests, raise an exception when trying to access the attribute."""
    def __init__(self, exception: Exception, message: str) -> None:
        self._message = message
        self._exception = exception

    def __getattribute__(self, name: str):
        """If an exception was raised during the setup of the tests, raise an exception when trying to access the attribute."""
        exception = object.__getattribute__(self, "_exception")
        if exception is not None and os.getenv("PYTEST_CURRENT_TEST"):
            exception_message = f"When during setup of the tests an error was raised: {exception}"
            if self._message:
                exception_message = f"{self._message} {exception_message}"
            raise ExceptionDuringTestSetupError() from exception
        return object.__getattribute__(self, name)

@pytest.fixture
def test_directory(request: pytest.FixtureRequest, snappylapy_settings: Settings) -> pathlib.Path:
    """Get the test directory for the test. Raise a better error message if the fixture is not parametrized."""
    try:
        return snappylapy_settings.snapshots_base_dir
    except Exception as e:
        error_msg = "The test_directory fixture is not parametrized, please add the snappylapy marker to the test, e.g. @pytest.mark.snappylapy(foreach_folder_in='test_data')"
        raise Exception(error_msg) from e

def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Generate parametrized tests for the pipeline output and input."""
    marker = metafunc.definition.get_closest_marker("snappylapy")
    if not marker:
        return
    foreach_folder_in: str | pathlib.Path = marker.kwargs.get("foreach_folder_in", None)
    if foreach_folder_in:
        test_cases = [p for p in pathlib.Path(foreach_folder_in).iterdir() if p.is_dir()]
        ids = [p.name for p in test_cases]
        metafunc.parametrize("snappylapy_settings", test_cases, indirect=True, ids=ids)
    depends = marker.kwargs.get("depends", []) if marker else []
    if depends:
        function_depends = marker.kwargs['depends'][0]
        if not hasattr(function_depends, "pytestmark"):
            return
        function_depends_marker: _pytest.mark.structures.Mark = function_depends.pytestmark[0]
        # It might be parametrized
        # Example: Mark(name='parametrize', args=('test_directory', ['test_data/case1', 'test_data/case2']), kwargs={})
        # Parametize the snappylapy_settings fixture
        if function_depends_marker.name == "parametrize":
            ids = function_depends_marker.kwargs.get("ids", None)
            metafunc.parametrize("snappylapy_settings", function_depends_marker.args[1], indirect=True, ids=ids)
        elif function_depends_marker.name == "snappylapy":
            foreach_folder_in = _get_kwargs_from_depend_function(depends[0], "snappylapy", "foreach_folder_in")
            if not foreach_folder_in:
                return
            test_cases = [p for p in pathlib.Path(foreach_folder_in).iterdir() if p.is_dir()]
            ids = [p.name for p in test_cases]
            metafunc.parametrize("snappylapy_settings", test_cases, indirect=True, ids=ids)
