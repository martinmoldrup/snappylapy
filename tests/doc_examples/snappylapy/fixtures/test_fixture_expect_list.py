import pytest
from snappylapy.fixtures import Expect

def test_expect_list(expect: Expect) -> None:
    data: list[int] = [1, 2, 3]
    expect.list(data).to_match_snapshot()