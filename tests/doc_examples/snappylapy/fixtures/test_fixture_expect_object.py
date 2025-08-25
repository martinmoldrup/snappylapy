import pytest
from snappylapy.fixtures import Expect

def test_expect_object(expect: Expect) -> None:
    obj: dict[str, str] = {"key": "value"}
    expect.object(obj).to_match_snapshot()