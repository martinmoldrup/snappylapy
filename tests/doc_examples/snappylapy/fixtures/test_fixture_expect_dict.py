import pytest
from snappylapy.fixtures import Expect

def test_expect_dict(expect: Expect) -> None:
    data: dict[str, str] = {"key": "value"}
    expect.dict(data).to_match_snapshot()
    expect.dict(data, name="snapshot_name", filetype="dict.json").to_match_snapshot()