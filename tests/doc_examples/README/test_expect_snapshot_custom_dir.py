import pytest
from snappylapy import Expect

@pytest.mark.snappylapy(output_dir="custom_dir")
def test_snapshot_with_custom_directories(expect: Expect):
    """Test snapshot with custom directories."""
    expect.string("Hello World").to_match_snapshot()