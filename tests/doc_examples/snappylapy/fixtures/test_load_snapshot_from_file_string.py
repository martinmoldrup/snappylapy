import pytest
from snappylapy.fixtures import LoadSnapshot, Expect

def test_save_string_snapshot(expect: Expect) -> None:
    message: str = "Hello, pytest!"
    expect(message).to_match_snapshot()

@pytest.mark.snappylapy(depends=[test_save_string_snapshot])
def test_load_snapshot_string(load_snapshot: LoadSnapshot) -> None:
    data: str = load_snapshot.string()
    assert data == "Hello, pytest!"