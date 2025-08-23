import pathlib
from snappylapy import Expect, LoadSnapshot
import json
import pytest

def test_snapshot_string(expect: Expect):
    """Test snapshot with string data."""
    expect.string("Hello World").to_match_snapshot()

def test_custom_type(expect: Expect):
    """Test snapshot with a custom type."""
    class CustomObject:
        """A custom type for snapshot."""
        pass

    expect(CustomObject()).to_match_snapshot()

def test_snapshot_bytes(expect: Expect):
    """Test snapshot with bytes data."""
    expect.bytes(b"Hello World", name="bytes_snapshot").to_match_snapshot()

def test_snapshot_dict(expect: Expect):
    """Test snapshot with dictionary data."""
    expect.dict({
        "name": "John Doe",
        "age": 31
    }).to_match_snapshot()

def test_snapshot_list(expect: Expect):
    """Test snapshot with list data."""
    expect.list(["John Doe", 31]).to_match_snapshot()

def test_snapshot_json_bytes(expect: Expect):
    """Test snapshot with JSON bytes data."""
    data = json.dumps({"name": "John Doe", "age": 31}).encode()
    expect.bytes(data, name="json_bytes_snapshot").to_match_snapshot()

@pytest.mark.snappylapy(depends=[test_snapshot_dict])
def test_load_snapshot_from_file(load_snapshot: LoadSnapshot):
    """Test loading snapshot data created in test_snapshot_dict from a file using the deserializer."""
    data = load_snapshot.dict()
    assert data == {"name": "John Doe", "age": 31}

@pytest.mark.snappylapy(depends=[test_snapshot_string])
def test_load_snapshot_from_file_string(load_snapshot: LoadSnapshot):
    """Test loading snapshot data created in test_snapshot_string from a file using the deserializer."""
    data = load_snapshot.string()
    assert data == "Hello World"


def test_snapshot_python_code(expect: Expect):
    """Test snapshot with Python code string."""
    py_code = "print('Hello World')"
    expect.string(py_code, filetype="py", name="python_code_snapshot").to_match_snapshot()

@pytest.mark.snappylapy(output_dir="custom_dir")
def test_snapshot_with_custom_directories(expect: Expect):
    """Test snapshot with custom directories."""
    expect.string("Hello World").to_match_snapshot()

@pytest.mark.snappylapy(depends=[test_snapshot_with_custom_directories])
def test_load_snapshot_from_custom_dir(load_snapshot: LoadSnapshot):
    """Test loading snapshot data created in test_snapshot_with_custom_directories from a file using the deserializer."""
    data = load_snapshot.string()
    assert data == "Hello World"

def test_snapshot_multiple_assertions(expect: Expect):
    """Test snapshot with multiple assertions."""
    expect.string("Hello World").to_match_snapshot()
    expect.dict({
        "name": "John Doe",
        "age": 31
    }).to_match_snapshot()

@pytest.mark.parametrize("data", [
    "Hello World",
    "Hello Galaxy",
    "Hello Universe",
])
def test_snapshot_parametrized(data: str, expect: Expect):
    """Test snapshot with parametrized data."""
    expect.string(data).to_match_snapshot()


@pytest.mark.snappylapy(foreach_folder_in="test_data")
def test_snapshot_multiple_folders_snappylapy_marker(test_directory: pathlib.Path, expect: Expect):
    """Test snapshot with multiple folders."""
    expect.string("Hello World").to_match_snapshot()

@pytest.mark.parametrize("test_directory", list(pathlib.Path("test_data").iterdir()), ids=lambda x: x.name)
def test_snapshot_multiple_folders_pytest_parametrize(test_directory: pathlib.Path, expect: Expect):
    """Test snapshot with multiple folders."""
    expect.string("Hello World").to_match_snapshot()

@pytest.mark.snappylapy(depends=[test_snapshot_multiple_folders_pytest_parametrize])
@pytest.mark.skip(reason="Functionaility not implemented yet.")
def test_load_parametrized_snapshot_from_file(load_snapshot: LoadSnapshot):
    """Test loading snapshot data created in test_snapshot_parametrized from a file using the deserializer."""
    data = load_snapshot.string()
    assert data == "Hello World"

@pytest.mark.snappylapy(depends=[test_snapshot_multiple_folders_snappylapy_marker])
def test_load_snapshot_from_multiple_folders(load_snapshot: LoadSnapshot):
    """Test loading snapshot data created in test_snapshot_multiple_folders from a file using the deserializer."""
    data = load_snapshot.string()
    assert data == "Hello World"