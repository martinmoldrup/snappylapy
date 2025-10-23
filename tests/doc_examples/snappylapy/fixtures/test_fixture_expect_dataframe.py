import pytest
from snappylapy.fixtures import Expect

try:
    import pandas as pd

    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


@pytest.mark.skipif(not HAS_PANDAS, reason="pandas is not installed")
def test_expect_dataframe(expect: Expect) -> None:
    """Test that dataframe matches the snapshot."""
    df: pd.DataFrame = pd.DataFrame({"key": ["value1", "value2"]})
    expect.dataframe(df).to_match_snapshot()
