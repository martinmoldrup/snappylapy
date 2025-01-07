import pytest
from pytest import Pytester

def test_snapshot_string(pytester: Pytester):
    """Test snapshot with string data."""
    test_code = """
    from snappylapy import Expect

    def test_snapshot_string(expect: Expect):
        expect.string("Hello World").to_match_snapshot()
    """
    pytester.makepyfile(test_code)
    result = pytester.runpytest('-v', '--snapshot-update')
    assert result.ret == 0
    result = pytester.runpytest('-v')
    assert result.ret == 0

def test_snapshot_bytes(pytester: Pytester):
    """Test snapshot with bytes data."""
    test_code = """
    from snappylapy import Expect

    def test_snapshot_bytes(expect: Expect):
        expect.bytes(b"Hello World", name="bytes_snapshot").to_match_snapshot()
    """
    pytester.makepyfile(test_code)
    result = pytester.runpytest('-v', '--snapshot-update')
    assert result.ret == 0
    result = pytester.runpytest('-v')
    assert result.ret == 0

def test_snapshot_dict(pytester: Pytester):
    """Test snapshot with dictionary data."""
    test_code = """
    from snappylapy import Expect

    def test_snapshot_dict(expect: Expect):
        expect.dict({
            "name": "John Doe",
            "age": 31
        }).to_match_snapshot()
    """
    pytester.makepyfile(test_code)
    result = pytester.runpytest('-v', '--snapshot-update')
    assert result.ret == 0
    result = pytester.runpytest('-v')
    assert result.ret == 0

def test_snapshot_list(pytester: Pytester):
    """Test snapshot with list data."""
    test_code = """
    from snappylapy import Expect

    def test_snapshot_list(expect: Expect):
        expect.list(["John Doe", 31]).to_match_snapshot()
    """
    pytester.makepyfile(test_code)
    result = pytester.runpytest('-v', '--snapshot-update')
    assert result.ret == 0
    result = pytester.runpytest('-v')
    assert result.ret == 0

def test_snapshot_json_bytes(pytester: Pytester):
    """Test snapshot with JSON bytes data."""
    test_code = """
    import json
    from snappylapy import Expect

    def test_snapshot_json_bytes(expect: Expect):
        data = json.dumps({"name": "John Doe", "age": 31}).encode()
        expect.bytes(data, name="json_bytes_snapshot").to_match_snapshot()
    """
    pytester.makepyfile(test_code)
    result = pytester.runpytest('-v', '--snapshot-update')
    assert result.ret == 0
    result = pytester.runpytest('-v')
    assert result.ret == 0

def test_snapshot_python_code(pytester: Pytester):
    """Test snapshot with Python code string."""
    test_code = """
    from snappylapy import Expect

    def test_snapshot_python_code(expect: Expect):
        py_code = "print('Hello World')"
        expect.string(py_code, filetype="py", name="python_code_snapshot").to_match_snapshot()
    """
    pytester.makepyfile(test_code)
    result = pytester.runpytest('-v', '--snapshot-update')
    assert result.ret == 0
    result = pytester.runpytest('-v')
    assert result.ret == 0

def test_snapshot_with_custom_directories(pytester: Pytester):
    """Test snapshot with custom directories."""
    test_code = """
    import pathlib
    from snappylapy import Expect

    def test_snapshot_with_custom_directories(expect: Expect):
        expect.snapshot_dir = pathlib.Path("__snapshots_other_location__")
        expect.test_results_dir = pathlib.Path("__test_results_other_location__")
        expect.string("Hello World").to_match_snapshot()
    """
    pytester.makepyfile(test_code)
    result = pytester.runpytest('-v', '--snapshot-update')
    assert result.ret == 0
    result = pytester.runpytest('-v')
    assert result.ret == 0

def test_snapshot_multiple_assertions(pytester: Pytester):
    """Test snapshot with multiple assertions."""
    test_code = """
    from snappylapy import Expect

    def test_snapshot_multiple_assertions(expect: Expect):
        expect.string("Hello World").to_match_snapshot()
        expect.dict({
            "name": "John Doe",
            "age": 31
        }).to_match_snapshot()
    """
    pytester.makepyfile(test_code)
    result = pytester.runpytest('-v', '--snapshot-update')
    assert result.ret == 0
    result = pytester.runpytest('-v')
    assert result.ret == 0
