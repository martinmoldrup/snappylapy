"""Pytest plugin for snapshot testing."""

from __future__ import annotations

import os
import re
import pytest
import pathlib
import _pytest.mark
from collections.abc import Callable
from snappylapy import Expect, LoadSnapshot
from snappylapy._utils_directories import DirectoryNamesUtil
from snappylapy.constants import DEFAULT_SNAPSHOT_BASE_DIR
from snappylapy.exceptions import TestDirectoryNotParametrizedError
from snappylapy.fixtures import Settings
from snappylapy.session import SnapshotSession
from typing import Any


def _get_kwargs_from_depend_function(
    depends_function: Callable,
    marker_name: str,
    kwags_key: str,
) -> str | None:
    """Get a test function with a pytest marker assigned and get a value from the marker."""
    if not hasattr(depends_function, "pytestmark"):
        return None
    marks: list[_pytest.mark.structures.Mark] = depends_function.pytestmark
    for mark in marks:
        if mark.name == marker_name:
            return mark.kwargs.get(kwags_key, None)
    return None


def _get_args_from_depend_function(
    depends_function: Callable,
    marker_name: str,
) -> tuple[Any] | None:
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
    update_snapshots = request.config.getoption("--snapshot-update")
    marker = request.node.get_closest_marker("snappylapy")
    match = re.search(r"\[(.*?)\]", request.node.name)
    param_name: str | None = match.group(1) if match else None
    settings = Settings(
        test_filename=request.module.__name__,
        test_function=request.node.originalname,
        custom_name=param_name,
        snapshot_update=update_snapshots,
    )
    if marker:
        output_dir: str | pathlib.Path = marker.kwargs.get("output_dir", None)
        if output_dir:
            settings.snapshots_base_dir = pathlib.Path(output_dir)
    path_output_dir: pathlib.Path | None = None
    if hasattr(request, "param"):
        path_output_dir = request.param
        if path_output_dir is None:
            # TODO: Add a better error message
            msg = "Path output directory cannot be None"
            raise ValueError(msg)
        settings.depending_snapshots_base_dir = pathlib.Path(path_output_dir)
        settings.snapshots_base_dir = pathlib.Path(path_output_dir)
        settings.custom_name = path_output_dir.name
    # If not parametrized, get the depends from the marker
    depends: list = marker.kwargs.get("depends", []) if marker else []
    if depends:
        input_dir_from_depends = _get_kwargs_from_depend_function(depends[0], "snappylapy", "output_dir")
        if input_dir_from_depends:
            path_output_dir = pathlib.Path(input_dir_from_depends)
        settings.depending_test_filename = depends[0].__module__
        settings.depending_test_function = depends[0].__name__
    settings.depending_snapshots_base_dir = path_output_dir or DEFAULT_SNAPSHOT_BASE_DIR
    return settings


@pytest.fixture
def expect(request: pytest.FixtureRequest, snappylapy_settings: Settings) -> Expect:
    """Initialize the snapshot object with update_snapshots flag from pytest option."""
    snappylapy_session: SnapshotSession = request.config.snappylapy_session  # type: ignore[attr-defined]
    return Expect(
        snappylapy_session=snappylapy_session,
        snappylapy_settings=snappylapy_settings,
    )


@pytest.fixture
def load_snapshot(snappylapy_settings: Settings) -> LoadSnapshot:
    """Initialize the LoadSnapshot object."""
    return LoadSnapshot(snappylapy_settings)


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
    """Initialize the snapshot session before running tests."""
    # Check if we're in discovery/collection mode
    if getattr(session.config.option, "collectonly", False) or getattr(session.config.option, "collect_only", False):
        return

    session.config.snappylapy_session = SnapshotSession()  # type: ignore[attr-defined]
    directory_util: DirectoryNamesUtil = DirectoryNamesUtil()
    files_to_delete: list[pathlib.Path] = directory_util.get_all_file_paths_test_results()
    for file_path in files_to_delete:
        file_path.unlink()


class ExceptionDuringTestSetupError(Exception):
    """Error raised when an exception is raised during the setup of the tests."""


class ReturnError:
    """Return an error when trying to access the attribute during the setup of the tests."""

    def __init__(self, exception: Exception, message: str) -> None:
        self._message = message
        self._exception = exception

    def __getattribute__(self, name: str) -> Any:  # noqa: ANN401
        """Raise an exception when trying to access the attribute, if exception was raised during the setup of tests."""
        exception = object.__getattribute__(self, "_exception")
        if exception is not None and os.getenv("PYTEST_CURRENT_TEST"):
            exception_message = f"When during setup of the tests an error was raised: {exception}"
            if self._message:
                exception_message = f"{self._message} {exception_message}"
            raise ExceptionDuringTestSetupError from exception
        return object.__getattribute__(self, name)


@pytest.fixture
def test_directory(snappylapy_settings: Settings) -> pathlib.Path:
    """Get the test directory for the test. Raise a better error message if the fixture is not parametrized."""
    try:
        return pathlib.Path(snappylapy_settings.snapshots_base_dir)
    except Exception as e:
        raise TestDirectoryNotParametrizedError from e


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Generate parametrized tests for the pipeline output and input."""
    marker = metafunc.definition.get_closest_marker("snappylapy")
    if not marker:
        return
    foreach_folder_in: str | pathlib.Path | None = marker.kwargs.get("foreach_folder_in", None)
    if foreach_folder_in:
        test_cases = [p for p in pathlib.Path(foreach_folder_in).iterdir() if p.is_dir()]
        ids = [p.name for p in test_cases]
        metafunc.parametrize("snappylapy_settings", test_cases, indirect=True, ids=ids)
    depends = marker.kwargs.get("depends", []) if marker else []
    if depends:
        function_depends = marker.kwargs["depends"][0]
        if not hasattr(function_depends, "pytestmark"):
            return
        function_depends_marker: _pytest.mark.structures.Mark = function_depends.pytestmark[0]
        # It might be parametrized
        # Example: Mark(name='parametrize', args=('test_directory', ['test_data/case1', 'test_data/case2']), kwargs={})
        # Parametize the snappylapy_settings fixture
        # if function_depends_marker.name == "parametrize":
        #     ids = function_depends_marker.kwargs.get("ids", None)
        #     metafunc.parametrize("snappylapy_settings", function_depends_marker.args[1], indirect=True, ids=ids)
        if function_depends_marker.name == "snappylapy":
            foreach_folder_in = _get_kwargs_from_depend_function(depends[0], "snappylapy", "foreach_folder_in")
            if not foreach_folder_in:
                return
            test_cases = [p for p in pathlib.Path(foreach_folder_in).iterdir() if p.is_dir()]
            ids = [p.name for p in test_cases]
            metafunc.parametrize("snappylapy_settings", test_cases, indirect=True, ids=ids)
