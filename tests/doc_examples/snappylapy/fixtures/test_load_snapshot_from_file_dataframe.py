import pytest
from snappylapy.fixtures import Expect, LoadSnapshot

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

@pytest.mark.skipif(not HAS_PANDAS, reason="pandas is not installed")
def test_save_dataframe_snapshot(expect: Expect) -> None:
    """Test saving a dataframe snapshot."""
    df: pd.DataFrame = pd.DataFrame({"numbers": [1, 2, 3]})
    expect(df).to_match_snapshot()

@pytest.mark.skipif(not HAS_PANDAS, reason="pandas is not installed")
@pytest.mark.snappylapy(depends=[test_save_dataframe_snapshot])
def test_load_snapshot_dataframe(load_snapshot: LoadSnapshot) -> None:
    """Test loading a dataframe snapshot."""
    df: pd.DataFrame = load_snapshot.dataframe()
    assert df["numbers"].sum() == 6