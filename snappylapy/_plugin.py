"""Pytest plugin for snapshot testing."""
import pytest
from snappylapy import Expect, LoadSnapshot
from snappylapy.fixtures import Settings


@pytest.fixture()
def expect(request: pytest.FixtureRequest) -> Expect:
    """Initialize the snapshot object with update_snapshots flag from pytest option."""
    update_snapshots = request.config.getoption("--snapshot-update")
    return Expect(
        update_snapshots=update_snapshots,
        test_filename=request.module.__name__,
        test_function=request.node.name,
    )


@pytest.fixture()
def load_snapshot(request: pytest.FixtureRequest) -> LoadSnapshot:
    """Initialize the LoadSnapshot object."""
    marker = request.node.get_closest_marker("snappylapy")
    depends = marker.kwargs.get("depends", []) if marker else []
    settings = Settings(
        test_filename=request.module.__name__,
        test_function=request.node.name,
    )
    if not depends:
        return LoadSnapshot(settings)

    settings.test_function = depends[0].__name__
    settings.test_filename = depends[0].__module__
    return LoadSnapshot(settings)


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
