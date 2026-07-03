"""Generate a large dictionary with data."""


def generate_large_dict(size: int = 100) -> dict[str, str]:
    return {f"key_{i}": f"value_{i}" for i in range(1, size)}

from snappylapy import Expect

def test_large_dict_snapshot(expect: Expect) -> None:
    data = generate_large_dict(1000)
    expect(data).to_match_snapshot()
