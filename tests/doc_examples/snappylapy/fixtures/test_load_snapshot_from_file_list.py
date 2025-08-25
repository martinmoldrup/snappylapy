import pytest
from typing import Any
from snappylapy import LoadSnapshot, Expect

def transform_data(data: list) -> list:
    return [x * 2 for x in data]

def next_transformation(data: list) -> list:
    return [x + 1 for x in data]

def test_transform_data(expect: Expect) -> None:
    data = [1, 2, 3]
    result = transform_data(data)
    expect(result).to_match_snapshot()

@pytest.mark.snappylapy(depends=[test_transform_data])
def test_next_transformation(load_snapshot: LoadSnapshot, expect: Expect) -> None:
    data: list[Any] = load_snapshot.list()
    result = next_transformation(data)
    expect(result).to_match_snapshot()