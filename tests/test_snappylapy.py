import pathlib
from snappylapy import Snapshot
import json


def test_step_1(snapshot: Snapshot):
    snapshot.snapshot_output_dir = pathlib.Path("__snapshots__")
    snapshot.test_results_output_dir = pathlib.Path("__test_results__")
    snapshot(b"Hello World")
    snapshot.assert_immutable()

def test_step_2(snapshot: Snapshot):
    data = json.dumps({"name": "John Doe", "age": 31}).encode()
    snapshot(data, name="dict_from_step_2")
    snapshot.assert_immutable()


def test_step_3(snapshot: Snapshot):
    py_code = b"print('Hello World')"
    snapshot(py_code, filetype="py")
    snapshot.assert_immutable()
