import pytest
from pytest import Pytester

def test_snapshot_string(pytester: Pytester):
    """Test snapshot with string data."""
    test_code = """
    from snappylapy import Expect

    def test_snapshot_string(expect: Expect):
        expect.string("Hello World").to_match_snapshot()
    """
    pytester.makepyfile(test_code=test_code)
    result = pytester.runpytest('-v', '--snapshot-update')
    assert result.ret == 0, "\n".join(result.outlines)
    result = pytester.runpytest('-v')
    assert result.ret == 0, "\n".join(result.outlines)

def test_fails_snapshot_not_exists(pytester: Pytester):
    """Test the failure of a snapshot when the snapshot data does not exist."""
    test_code = """
    from snappylapy import Expect

    def test_fails_snapshot_string(expect: Expect):
        expect.string("Hello World").to_match_snapshot()
    """
    pytester.makepyfile(test_code=test_code)
    result = pytester.runpytest('-v')
    assert result.ret == 1, "\n".join(result.outlines)

def test_fails_snapshot_string_mismatch(pytester: Pytester):
    """Test the failure of a snapshot when the snapshot data does not match."""
    test_code = """
    from snappylapy import Expect

    def test_fails_snapshot_string(expect: Expect):
        expect.string("Hello World", name="string_snapshot").to_match_snapshot()
    """
    pytester.makepyfile(test_code=test_code)
    result = pytester.runpytest('-v', '--snapshot-update', '--cache-clear')
    assert result.ret == 0, "\n".join(result.outlines)
    
    # Modify the test so it return a different value
    test_code = """
    from snappylapy import Expect

    def test_fails_snapshot_string(expect: Expect):
        expect.string("Hello World!", name="string_snapshot").to_match_snapshot()
    """
    pytester.makepyfile(test_code=test_code)

    result = pytester.runpytest('-v')
    assert result.ret == 1, "\n".join(result.outlines)
    result.stdout.fnmatch_lines([
        '*- Hello World!',
        '*+ Hello World',
    ])


def test_fails_snapshot_list_mismatch(pytester: Pytester):
    """Test the failure of a snapshot when the snapshot data does not match."""
    test_code = """
    from snappylapy import Expect

    def test_fails_snapshot_string(expect: Expect):
        expect.list(["John Doe", 31]).to_match_snapshot()
    """
    pytester.makepyfile(test_code=test_code)
    result = pytester.runpytest('-v', '--snapshot-update', '--cache-clear')
    assert result.ret == 0, "\n".join(result.outlines)
    
    # Modify the test so it return a different value
    test_code = """
    from snappylapy import Expect

    def test_fails_snapshot_string(expect: Expect):
        expect.list(["John Doe 2", 31]).to_match_snapshot()
    """
    pytester.makepyfile(test_code=test_code)

    result = pytester.runpytest("-v")
    assert result.ret == 1, "\n".join(result.outlines)
    assert 'E                 -   "John Doe 2",' in result.stdout.lines
    assert 'E                 +   "John Doe",' in result.stdout.lines
    # result.stdout.fnmatch_lines([
    #     '*- ["John Doe 2", 31]',
    #     '*+ ["John Doe", 31]',
    # ])

@pytest.mark.skip(reason="This fails under certain conditions. The second run of the tests do not get the new dict, I suspect it is due to a problem in pytester, not the snappylapy code. It is only a problem when the first element does not differ")
def test_fails_snapshot_dict2_mismatch(pytester: Pytester) -> None:
    """Test the failure of a snapshot when the dict snapshot data does not match."""
    test_code: str = """
    from snappylapy import Expect

    def test_fails_snapshot_dict(expect: Expect):
        expect.dict({
            "name": "John Doe",
            "age": 31
        }).to_match_snapshot()
    """
    pytester.makepyfile(test_code=test_code)
    result = pytester.runpytest('-v', '--snapshot-update', '--cache-clear')
    assert result.ret == 0, "\n".join(result.outlines)

    # Delete the test_code.py file
    if not pytester.path.joinpath("test_code.py").exists():
        raise FileNotFoundError("test_code.py file not found.")
    (pytester.path / "test_code.py").unlink()

    # Modify the test so it returns a different value
    test_code = """
    from snappylapy import Expect

    def test_fails_snapshot_dict(expect: Expect):
        expect.dict({
            "name": "John Doe",
            "age": 32,
        }).to_match_snapshot()
    """
    pytester.makepyfile(test_code=test_code)

    result = pytester.runpytest('-v', '-s', '--cache-clear')
    result.stdout.fnmatch_lines([
        '*- {"name": "John Doe 2", "age": 31}',
        '*+ {"name": "John Doe", "age": 31}',
    ])
    assert result.ret == 1, "\n".join(result.outlines)

def test_fails_snapshot_dict_mismatch(pytester: Pytester) -> None:
    """Test the failure of a snapshot when the dict snapshot data does not match."""
    test_code: str = """
    from snappylapy import Expect

    def test_fails_snapshot_dict(expect: Expect):
        expect.dict({
            "name": "John Doe",
            "age": 31
        }).to_match_snapshot()
    """
    pytester.makepyfile(test_code=test_code)
    result = pytester.runpytest('-v', '--snapshot-update', '--cache-clear')
    assert result.ret == 0, "\n".join(result.outlines)

    # Delete the test_code.py file
    if not pytester.path.joinpath("test_code.py").exists():
        raise FileNotFoundError("test_code.py file not found.")
    (pytester.path / "test_code.py").unlink()

    # Modify the test so it returns a different value
    test_code = """
    from snappylapy import Expect

    def test_fails_snapshot_dict(expect: Expect):
        expect.dict({
            "name": "John Doe 2",
            "age": 31,
        }).to_match_snapshot()
    """
    pytester.makepyfile(test_code=test_code)

    result = pytester.runpytest('-v', '-s', '--cache-clear')
    result.stdout.fnmatch_lines([
        '*-   "name": "John Doe 2",',
        '*+   "name": "John Doe",',
    ])
    assert result.ret == 1, "\n".join(result.outlines)


def test_fails_snapshot_bytes_mismatch(pytester: Pytester):
    """Test the failure of a snapshot when the snapshot data does not match."""
    test_code = """
    from snappylapy import Expect

    def test_fails_snapshot_bytes(expect: Expect):
        expect.bytes(b"Hello World", name="bytes_snapshot").to_match_snapshot()
    """
    pytester.makepyfile(test_code=test_code)
    result = pytester.runpytest('-v', '--snapshot-update', '--cache-clear')
    assert result.ret == 0, "\n".join(result.outlines)
    
    # Modify the test so it return a different value
    test_code = """
    from snappylapy import Expect

    def test_fails_snapshot_bytes(expect: Expect):
        expect.bytes(b"Hello World!", name="bytes_snapshot").to_match_snapshot()
    """
    pytester.makepyfile(test_code=test_code)

    result = pytester.runpytest('-v')
    assert result.ret == 1, "\n".join(result.outlines)
    result.stdout.fnmatch_lines([
        '*- Hello World!',
        '*+ Hello World',
    ])
    print(result.outlines)

def test_snapshot_bytes(pytester: Pytester):
    """Test snapshot with bytes data."""
    test_code = """
    from snappylapy import Expect

    def test_snapshot_bytes(expect: Expect):
        expect.bytes(b"Hello World", name="bytes_snapshot").to_match_snapshot()
    """
    pytester.makepyfile(test_code)
    result = pytester.runpytest('-v', '--snapshot-update')
    assert result.ret == 0, "\n".join(result.outlines)
    result = pytester.runpytest('-v')
    assert result.ret == 0, "\n".join(result.outlines)

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
    assert result.ret == 0, "\n".join(result.outlines)
    result = pytester.runpytest('-v')
    assert result.ret == 0, "\n".join(result.outlines)

def test_snapshot_list(pytester: Pytester):
    """Test snapshot with list data."""
    test_code = """
    from snappylapy import Expect

    def test_snapshot_list(expect: Expect):
        expect.list(["John Doe", 31]).to_match_snapshot()
    """
    pytester.makepyfile(test_code)
    result = pytester.runpytest('-v', '--snapshot-update')
    assert result.ret == 0, "\n".join(result.outlines)
    result = pytester.runpytest('-v')
    assert result.ret == 0, "\n".join(result.outlines)

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
    assert result.ret == 0, "\n".join(result.outlines)
    result = pytester.runpytest('-v')
    assert result.ret == 0, "\n".join(result.outlines)

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
    assert result.ret == 0, "\n".join(result.outlines)
    result = pytester.runpytest('-v')
    assert result.ret == 0, "\n".join(result.outlines)

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
    assert result.ret == 0, "\n".join(result.outlines)
    result = pytester.runpytest('-v')
    assert result.ret == 0, "\n".join(result.outlines)

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
    assert result.ret == 0, "\n".join(result.outlines)
    result = pytester.runpytest('-v')
    assert result.ret == 0, "\n".join(result.outlines)


def test_load_snapshot_from_file(pytester: Pytester):
    """Test loading snapshot data created in test_snapshot_dict from a file using the deserializer."""
    test_code = """
    from snappylapy import LoadSnapshot, Expect
    import pytest

    def test_snapshot_dict(expect: Expect):
        expect.dict({
            "name": "John Doe",
            "age": 31
        }).to_match_snapshot()

    @pytest.mark.snappylapy(depends=[test_snapshot_dict])
    def test_load_snapshot_from_file(load_snapshot: LoadSnapshot):
        data = load_snapshot.dict()
        assert data == {"name": "John Doe", "age": 31}
    """
    pytester.makepyfile(test_code)
    result = pytester.runpytest('-v', '--snapshot-update')
    assert result.ret == 0, "\n".join(result.outlines)


def test_load_snapshot_from_file_test_in_seperate_module(pytester: Pytester):
    """Check that the reordering of tests based on dependencies works."""
    create_snapshot_test_code = """
    from snappylapy import Expect

    def test_snapshot_dict(expect: Expect):
        expect.dict({
            "name": "John Doe",
            "age": 31
        }).to_match_snapshot()
    """
    load_snapshot_test_code = """
    from snappylapy import LoadSnapshot
    import test_create_snapshot
    import pytest

    @pytest.mark.snappylapy(depends=[test_create_snapshot.test_snapshot_dict])
    def test_load_snapshot_from_file(load_snapshot: LoadSnapshot):
        data = load_snapshot.dict()
        assert data == {"name": "John Doe", "age": 31}
    """

    pytester.makepyfile(test_create_snapshot=create_snapshot_test_code)
    pytester.makepyfile(test_a_load_snapshot=load_snapshot_test_code)
    result = pytester.runpytest('-v', '--snapshot-update')
    assert result.ret == 0, "\n".join(result.outlines)
