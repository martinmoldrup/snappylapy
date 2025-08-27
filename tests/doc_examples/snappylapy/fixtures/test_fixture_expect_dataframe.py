import pytest
try:
    import pandas as pd  # noqa: F401
    pandas_installed = True
except ImportError:
    pandas_installed = False
from snappylapy.fixtures import Expect

@pytest.mark.skipif(not pandas_installed, reason="pandas is not installed")
def test_expect_dataframe(expect: Expect) -> None:
    df: pd.DataFrame = pd.DataFrame({"key": ["value1", "value2"]})
    expect.dataframe(df).to_match_snapshot()