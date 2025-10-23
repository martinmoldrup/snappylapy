import json
import pytest
import pathlib
from typing import Any


def transform_data(data: dict) -> dict:
    """A sample transformation function."""
    # Example transformation: add a new key-value pair
    data["transformed"] = True
    return data

@pytest.mark.skip
@pytest.mark.snappylapy(foreach_folder_in="test_data")
def test_snapshot_parametrized_multiple_test_case_folders(test_directory: pathlib.Path, expect: Any) -> None:
    """Test snapshot with multiple folders."""
    data = json.loads((test_directory / "input.json").read_text())
    transformed_data = transform_data(data)
    expect.dict(transformed_data).to_match_snapshot()
