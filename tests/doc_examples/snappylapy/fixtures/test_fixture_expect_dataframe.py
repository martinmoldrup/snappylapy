import pytest
import pandas as pd
from snappylapy.fixtures import Expect

def test_expect_dataframe(expect: Expect) -> None:
    df: pd.DataFrame = pd.DataFrame({"key": ["value1", "value2"]})
    expect.dataframe(df).to_match_snapshot()