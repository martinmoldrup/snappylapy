import pytest
from snappylapy import Expect, LoadSnapshot


class Custom:
    def __init__(self) -> None:
        self.value = 42


def test_save_object_snapshot(expect: Expect) -> None:
    obj = Custom()
    expect(obj).to_match_snapshot()


@pytest.mark.snappylapy(depends=[test_save_object_snapshot])
def test_load_snapshot_object(load_snapshot: LoadSnapshot) -> None:
    obj = load_snapshot.object()
    assert hasattr(obj, "value")
    assert obj.value == 42
