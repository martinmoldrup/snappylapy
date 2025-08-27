import pytest
from snappylapy.fixtures import LoadSnapshot, Expect

def create_dict() -> dict[str, int]:
    return {"apples": 3, "bananas": 5}

def test_save_dict_snapshot(expect: Expect) -> None:
    data: dict[str, int] = create_dict()
    expect(data).to_match_snapshot()

@pytest.mark.snappylapy(depends=[test_save_dict_snapshot])
def test_load_snapshot_dict(load_snapshot: LoadSnapshot) -> None:
    data: dict[str, int] = load_snapshot.dict()
    assert data["apples"] == 3
    assert data["bananas"] == 5