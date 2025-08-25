from snappylapy import Expect

def generate_dict(size: int) -> dict[str, int]:
    """Function to test."""
    return {f"key_{i}": i for i in range(size)}

def test_snapshot_dict(expect: Expect):
    """Test snapshot with dictionary data."""
    data: dict = generate_dict(100)
    expect(data).to_match_snapshot()
    # or expect.dict(data).to_match_snapshot()