"""
Pytest plugin for snapshot testing.
"""
from typing import List
import pytest
from snappylapy import Expect, LoadSnapshot
from snappylapy.snappylapy import Settings



@pytest.fixture
def expect(request) -> Expect:
    """Initialize the snapshot object with update_snapshots flag from pytest option."""
    update_snapshots = request.config.getoption("--snapshot-update")
    return Expect(update_snapshots=update_snapshots)

@pytest.fixture
def load_snapshot(request: pytest.FixtureRequest) -> LoadSnapshot:
    """Initialize the LoadSnapshot object."""
    marker = request.node.get_closest_marker("snappylapy")
    depends = marker.kwargs.get("depends", []) if marker else []
    if not depends:
        return LoadSnapshot(Settings())
    
    filename = depends[0].__name__
    settings = Settings(
        filename_base=filename,
    )
    return LoadSnapshot(settings)

class SnappylapyPlugin:
    """Plugin for sorting the tests based on the dependencies."""
    @pytest.hookimpl(tryfirst=True)
    def pytest_collection_modifyitems(self, config: pytest.Config, items: List[pytest.Function]):
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

def pytest_configure(config: pytest.Config):
    """
    Register the "snappylapy" marker and configure the plugin,
    depending on the CLI options.
    """
    config.addinivalue_line("markers", "snappylapy: mark test to load snapshot data from a file.")
    config.pluginmanager.register(SnappylapyPlugin())

def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting")
    group.addoption(
        "--snapshot-update",
        action="store_true",
        dest="snapshot_update",
        default=False,
        help="update snapshots.",
    )




