import pytest
from snappylapy import Expect, LoadSnapshot

def test_snapshot_dict(expect: Expect):
    """Test snapshot with dictionary data.****"""
    expect({
        "name": "John Doe",
        "age": 31
    }).to_match_snapshot()

@pytest.mark.snappylapy(depends=[test_snapshot_dict])
def test_load_snapshot_from_file(load_snapshot: LoadSnapshot):
    """Test loading snapshot data created in test_snapshot_dict from a file using the deserializer."""
    data = load_snapshot.dict()
    # Normally you would use the data as an input for some other function
    # For demonstration, we will just assert the data matches the expected snapshot
    assert data == {"name": "John Doe", "age": 31}