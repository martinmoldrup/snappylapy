"""Testing of the string test expectations class."""
import pytest
import pathlib
import snappylapy.expectation_classes.expect_dataframe as module_on_test
from snappylapy.models import Settings
from unittest import mock

try:
    import pandas as pd  # noqa: F401
    pandas_installed = True
except ImportError:
    pandas_installed = False

@pytest.fixture
def expect() -> module_on_test.DataframeExpect:
    snappylapy_session = mock.MagicMock()
    return module_on_test.DataframeExpect(
        settings=Settings(
            test_filename="test_file",
            test_function="test_function",
        ),
        snappylapy_session=snappylapy_session,
    )

# @pytest.mark.skipif(not pandas_installed, reason="pandas is not installed")
# def test_to_match_snapshot(expect: module_on_test.DataframeExpect) -> None:
#     """Test the to_match_snapshot method of DataframeExpect."""
#     # TODO This will not actually create a snapshot with the snapshot session
#     dataframe_to_test = pd.DataFrame({"key": ["value1", "value2"]})
#     expect(dataframe_to_test).to_match_snapshot()

@pytest.mark.skipif(not pandas_installed, reason="pandas is not installed")
def test_columns_not_to_contain_nulls(expect: module_on_test.DataframeExpect) -> None:
    """Test the columns_not_to_contain_nulls method of DataframeExpect."""
    dataframe_to_test = pd.DataFrame({"key": ["value1", "value2"]})
    expect(dataframe_to_test).columns_not_to_contain_nulls()

@pytest.mark.skipif(not pandas_installed, reason="pandas is not installed")
def test_column_not_to_contain_nulls_fails(expect: module_on_test.DataframeExpect) -> None:
    """Test the column_not_to_contain_nulls method of DataframeExpect with failure."""
    dataframe_to_test = pd.DataFrame({"key": ["value1", "value2", None]})
    with pytest.raises(ValueError, match="Column key contains 1 null values"):
        expect(dataframe_to_test).column_not_to_contain_nulls("key")

@pytest.mark.skipif(not pandas_installed, reason="pandas is not installed")
def test_multiple_columns_not_to_contain_nulls_fails(expect: module_on_test.DataframeExpect) -> None:
    """Test the columns_not_to_contain_nulls method of DataframeExpect with failure."""
    dataframe_to_test = pd.DataFrame({"key1": ["value1", "value2"], "key2": [None, "value4"]})
    with pytest.raises(ValueError, match="Column key2 contains 1 null values"):
        expect(dataframe_to_test).columns_not_to_contain_nulls(["key1", "key2"])

@pytest.mark.skipif(not pandas_installed, reason="pandas is not installed")
def test_column_not_to_contain_nulls_fails_no_data(expect: module_on_test.DataframeExpect) -> None:
    """Test the column_not_to_contain_nulls method of DataframeExpect with no data."""
    with pytest.raises(ValueError, match="No data to check. Call __call__ first."):
        expect.column_not_to_contain_nulls("key")

@pytest.mark.skipif(not pandas_installed, reason="pandas is not installed")
def test_columns_to_match_regex(
    expect: module_on_test.DataframeExpect,
) -> None:
    """Test the columns_to_match_regex method of DataframeExpect."""
    dataframe_to_test = pd.DataFrame({"key1": ["value1", "value2"], "key2": ["test1", "test2"]})
    expect(dataframe_to_test).columns_to_match_regex({"key1": r"value\d", "key2": r"test\d"})
