import pytest
from snappylapy.fixtures import LoadSnapshot, Expect

def test_save_bytes_snapshot(expect: Expect) -> None:
    data: bytes = b"\x01\x02\x03"
    expect(data).to_match_snapshot()

@pytest.mark.snappylapy(depends=[test_save_bytes_snapshot])
def test_load_snapshot_bytes(load_snapshot: LoadSnapshot) -> None:
    data: bytes = load_snapshot.bytes()
    assert data == b"\x01\x02\x03"