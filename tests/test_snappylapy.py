import pathlib
from snappylapy import Expect
import json

def test_snapshot_string(expect: Expect):
    """Test snapshot with string data."""
    expect.string("Hello World").to_match_snapshot()

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

def test_snapshot_python_code(expect: Expect):
    """Test snapshot with Python code string."""
    py_code = "print('Hello World')"
    expect.string(py_code, filetype="py", name="python_code_snapshot").to_match_snapshot()

def test_snapshot_with_custom_directories(expect: Expect):
    """Test snapshot with custom directories."""
    expect.snapshot_dir = pathlib.Path("__snapshots_other_location__")
    expect.test_results_dir = pathlib.Path("__test_results_other_location__")
    expect.string("Hello World").to_match_snapshot()

def test_snapshot_multiple_assertions(expect: Expect):
    """Test snapshot with multiple assertions."""
    expect.string("Hello World").to_match_snapshot()
    expect.dict({
        "name": "John Doe",
        "age": 31
    }).to_match_snapshot()
