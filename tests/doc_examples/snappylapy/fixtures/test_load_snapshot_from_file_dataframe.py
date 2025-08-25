import pytest
import pandas as pd
from snappylapy.fixtures import LoadSnapshot, Expect

def test_save_dataframe_snapshot(expect: Expect) -> None:
    df: pd.DataFrame = pd.DataFrame({"numbers": [1, 2, 3]})
    expect(df).to_match_snapshot()

@pytest.mark.snappylapy(depends=[test_save_dataframe_snapshot])
def test_load_snapshot_dataframe(load_snapshot: LoadSnapshot) -> None:
    df: pd.DataFrame = load_snapshot.dataframe()
    assert df["numbers"].sum() == 6