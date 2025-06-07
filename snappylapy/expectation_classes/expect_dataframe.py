"""Snapshot testing and expectations for dicts."""

from __future__ import annotations

import pandas as pd
from .base_snapshot import BaseSnapshot
from snappylapy.serialization import JsonPickleSerializer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypeAlias


class DataframeExpect(BaseSnapshot[pd.DataFrame]):
    """Snapshot testing for dataframes."""

    serializer_class = JsonPickleSerializer[pd.DataFrame]
    DataFrame: TypeAlias = pd.DataFrame

    def __call__(
        self,
        data_to_snapshot: pd.DataFrame,
        name: str | None = None,
        filetype: str = "dataframe.json",
    ) -> DataframeExpect:
        """Prepare a dataframe for snapshot testing."""
        self._prepare_test(data_to_snapshot, name, filetype)
        return self

    def column_not_to_contain_nulls(
        self,
        column_name: str,
    ) -> DataframeExpect:
        """Check that a column does not contain null values."""
        if self._data is None:
            error_message = "No data to check. Call __call__ first."
            raise ValueError(error_message)
        if column_name not in self._data.columns:
            error_message = f"Column {column_name} not found in dataframe."
            raise ValueError(error_message)
        if self._data[column_name].isna().any():
            null_count: int = int(self._data[column_name].isna().sum())
            top_n: int = 3  # Number of examples to display
            null_rows: pd.DataFrame = self._data[self._data[column_name].isna()].head(top_n)
            null_value_error_message = (
                f"Column {column_name} contains {null_count} null values. "
                f"Top {top_n} examples:\n{null_rows.to_string(index=False)}"
            )
            raise ValueError(
                null_value_error_message,
            )
        return self

    def columns_not_to_contain_nulls(
        self,
        column_names: list[str] | None = None,
    ) -> DataframeExpect:
        """Check that multiple columns do not contain null values."""
        if self._data is None:
            error_message = "No data to check. Call __call__ first."
            raise ValueError(error_message)
        if not column_names:
            # Check all columns
            column_names = self._data.columns.tolist()
        assert column_names is not None, "Column names should have been set to default to all columns."
        error_texts: list[str] = []
        for column_name in column_names:
            try:
                self.column_not_to_contain_nulls(column_name)
            except ValueError as e:  # noqa: PERF203
                error_texts.append(str(e))
        if error_texts:
            raise ValueError("\n".join(error_texts))
        return self

    def columns_to_match_regex(
        self,
        column_to_regex: dict[str, str],
    ) -> DataframeExpect:
        """
        Check that columns match regex.

        column_to_regex: dict[str, str]
            Dictionary of column names to regex patterns.
            The column name is the key and the regex pattern is the value.
        """
        if self._data is None:
            error_message = "No data to check. Call __call__ first."
            raise ValueError(error_message)
        for column_name, regex in column_to_regex.items():
            if column_name not in self._data.columns:
                error_message = f"Column {column_name} not found in dataframe."
                raise ValueError(error_message)
            if not self._data[column_name].astype(str).str.match(regex).all():
                regex_mismatch_message = (
                    f"Column {column_name} does not match regex {regex}. "
                    f"Top 3 examples:\n{self._data[column_name].head(3).to_string(index=False)}"
                )
                raise ValueError(
                    regex_mismatch_message,
                )
        return self
