"""Pytest plugin for snapshot testing."""
import pathlib
from typing import Any
import pytest
import _pytest.mark
from snappylapy import Expect, LoadSnapshot
from snappylapy.fixtures import Settings
from snappylapy.session import SnapshotSession
from snappylapy.constants import DEFEAULT_SNAPSHOT_BASE_DIR


@pytest.fixture
def expect(request: pytest.FixtureRequest) -> Expect:
    """Initialize the snapshot object with update_snapshots flag from pytest option."""
    marker = request.node.get_closest_marker("snappylapy")
    update_snapshots = request.config.getoption("--snapshot-update")
    snappylapy_session: SnapshotSession = request.config.snappylapy_session  # type: ignore[attr-defined]
    output_dir = marker.kwargs.get("output_dir", None) if marker else None
    return Expect(
        update_snapshots=update_snapshots,
        test_filename=request.module.__name__,
        test_function=request.node.name,
        snappylapy_session=snappylapy_session,
        output_dir=output_dir,
    )

def _get_kwargs_from_depend_function(depends_function, marker_name: str, kwags_key: str) -> Any:
    """Get a test function with a pytest marker assigned and get a value from the marker."""
    if not hasattr(depends_function, "pytestmark"):
        return None
    marks: list[_pytest.mark.structures.Mark] = depends_function.pytestmark
    for mark in marks:
        if mark.name == marker_name:
            return mark.kwargs.get(kwags_key, None)
    return None



@pytest.fixture
def load_snapshot(request: pytest.FixtureRequest) -> LoadSnapshot:
    """Initialize the LoadSnapshot object."""
    marker = request.node.get_closest_marker("snappylapy")
    depends = marker.kwargs.get("depends", []) if marker else []
    output_dir = marker.kwargs.get("output_dir", None) if marker else None
    input_dir_from_depends = _get_kwargs_from_depend_function(depends[0], "snappylapy", "output_dir") if depends else None
    read_from_dir = pathlib.Path(input_dir_from_depends) if input_dir_from_depends else DEFEAULT_SNAPSHOT_BASE_DIR
    settings = Settings(
        test_filename=request.module.__name__,
        test_function=request.node.name,
    )
    if output_dir:
        settings.snapshots_base_dir = output_dir
    if not depends:
        return LoadSnapshot(settings, read_from_dir)

    settings.test_function = depends[0].__name__
    settings.test_filename  = depends[0].__module__
    return LoadSnapshot(settings, read_from_dir)


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
