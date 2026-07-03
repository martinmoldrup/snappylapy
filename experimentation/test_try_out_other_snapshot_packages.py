"""
Want to see how other snapshot packages do reporting when snapshots do not match and when they are updated.

pytest .\experimentation\test_try_out_other_snapshot_packages.py --snapshot-update
pytest .\experimentation\test_try_out_other_snapshot_packages.py --insta 
"""
import pytest
from json import dumps
import pytest_insta


@pytest.mark.skip
def test_snapshot_snapshottest(snapshot):
    """
    Test the snapshot dict.
    
    pip install pytest-snapshot
    pip install snapshottest
    """
    data = {"key": "value", "key2": "value2"}
    data_str = dumps(data, indent=4)
    snapshot.assert_match(data_str, "test_snapshot_dict")

class ObjectToSnapshot:
    def __init__(self, key, value):
        self.key = key
        self.value = value

@pytest.mark.skip
def test_snapshot_snapshottest_obj(snapshot):
    """
    Test the snapshot dict.
    
    pip install pytest-snapshot
    pip install snapshottest
    """
    data = ObjectToSnapshot("key", "value")
    snapshot.assert_match(data, "test_snapshot_dict")


@pytest.mark.skip
def test_snapshot_syrupy(snapshot):
    """
    Test the snapshot dict.
    
    pip install syrupy
    """
    data = {"key": "value", "key2": "value2"}
    data_str = dumps(data, indent=4)
    assert data_str == snapshot

def test_snapshot_pytest_insta2(snapshot):
    """
    Test the snapshot dict.
    
    pip install pytest-insta
    """
    data = {"key": "value", "key2": "value3"}
    data_str = dumps(data, indent=4)
    assert snapshot() == data_str




if __name__ == "__main__":
    print(__file__)
    pytest.main(["experimentation"])
