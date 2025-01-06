"""
Pytest plugin for snapshot testing.
"""
import pytest
from snappylapy import Expect



@pytest.fixture
def expect(request) -> Expect:
    """Initialize the snapshot object with update_snapshots flag from pytest option."""
    update_snapshots = request.config.getoption("--snapshot-update")
    return Expect(update_snapshots=update_snapshots)



def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting")
    group.addoption(
        "--snapshot-update",
        action="store_true",
        dest="snapshot_update",
        default=False,
        help="update snapshots.",
    )




