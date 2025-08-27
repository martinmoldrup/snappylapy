import pytest
from snappylapy.fixtures import LoadSnapshot, Expect

try:
    import pandas as pd  # noqa: F401
    pandas_installed = True
except ImportError:
    pandas_installed = False

@pytest.mark.skipif(not pandas_installed, reason="pandas is not installed")
def test_save_dataframe_snapshot(expect: Expect) -> None:
    df: pd.DataFrame = pd.DataFrame({"numbers": [1, 2, 3]})
    expect(df).to_match_snapshot()

@pytest.mark.skipif(not pandas_installed, reason="pandas is not installed")
@pytest.mark.snappylapy(depends=[test_save_dataframe_snapshot])
def test_load_snapshot_dataframe(load_snapshot: LoadSnapshot) -> None:
    df: pd.DataFrame = load_snapshot.dataframe()
    assert df["numbers"].sum() == 6