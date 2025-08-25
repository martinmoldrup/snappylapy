import pytest
from snappylapy.fixtures import Expect

def test_expect_bytes(expect: Expect) -> None:
    data: bytes = b"binary data"
    expect.bytes(data).to_match_snapshot()