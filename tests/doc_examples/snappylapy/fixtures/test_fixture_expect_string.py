import pytest
from snappylapy.fixtures import Expect

def test_expect_string(expect: Expect) -> None:
    data: str = "Hello, World!"
    expect.string(data).to_match_snapshot()