"""
The assertions are different for each file, but ideally we only want the snapshot object.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, Generic, List, Optional, Union, Callable, Type, TypeVar

T = TypeVar('T')

class BaseAssertion(Generic[T]):
    def __init__(self, element: Any, parent: "SnapshotWithAssertions") -> None:
        self._element = element
        self._parent = parent

    def __call__(self, element: T) -> None:
        self._parent.__call__(element)

class DictAssertions(BaseAssertion[dict]):
    """Assertions for dictionary objects."""
    def assert_equal(self) -> None: ...
    def assert_is_json_serializable(self) -> None: ...
    def assert_follows_schema(self) -> None: ...
    def has_same_keys(self) -> None: ...

class ListAssertions(BaseAssertion[list]):
    """Assertions for list objects."""
    def assert_equal(self) -> None: ...
    def assert_is_json_serializable(self) -> None: ...
    def assert_follows_schema(self) -> None: ...
    def has_same_length(self) -> None:
        """Asserts that the snapshot has the same length as the expected list."""

class StringAssertions(BaseAssertion[str]):
    """Assertions for string objects."""
    def assert_equal(self) -> None: ...
    def assert_is_approximately_equal(self) -> None: ...
    def assert_is_same_length(self) -> None: ...
    def assert_is_approximately_same_length(self) -> None: ...
    def assert_has_same_words(self) -> None: ...
    def assert_has_cosine_similarity(self) -> None: ...

class PandasDataFrameAssertions(BaseAssertion):
    """Assertions for pandas DataFrame objects."""
    def assert_equal(self) -> None: ...
    def assert_is_json_serializable(self) -> None: ...
    def assert_follows_schema(self) -> None: ...
    def has_same_shape(self) -> None: ...
    def has_same_columns(self) -> None: ...
    def has_same_index(self) -> None: ...

class PandasSeriesAssertions(BaseAssertion):
    """Assertions for pandas Series objects."""
    def assert_equal(self) -> None: ...
    def assert_is_json_serializable(self) -> None: ...
    def assert_follows_schema(self) -> None: ...
    def has_same_shape(self) -> None: ...
    def has_same_index(self) -> None: ...

class BytesAssertions(BaseAssertion[bytes]):
    """Assertions for bytes objects."""
    def assert_equal(self) -> None: ...
    def assert_is_json_serializable(self) -> None: ...
    def assert_follows_schema(self) -> None: ...



class SnapshotWithAssertions:
    def __init__(self) -> None:
        self._dict: Optional[DictAssertions] = None
        self._list: Optional[ListAssertions] = None
        self._string: Optional[StringAssertions] = None
        self._pandas_dataframe: Optional[PandasDataFrameAssertions] = None
        self._pandas_series: Optional[PandasSeriesAssertions] = None

    @property
    def dict(self) -> DictAssertions:
        if self._dict is None:
            self._dict = DictAssertions(self._element, self)
        return self._dict

    @property
    def list(self) -> ListAssertions:
        if self._list is None:
            self._list = ListAssertions(self._element, self)
        return self._list

    @property
    def string(self) -> StringAssertions:
        if self._string is None:
            self._string = StringAssertions(self._element, self)
        return self._string

    @property
    def pandas_dataframe(self) -> PandasDataFrameAssertions:
        if self._pandas_dataframe is None:
            self._pandas_dataframe = PandasDataFrameAssertions(self._element, self)
        return self._pandas_dataframe

    @property
    def pandas_series(self) -> PandasSeriesAssertions:
        if self._pandas_series is None:
            self._pandas_series = PandasSeriesAssertions(self._element, self)
        return self._pandas_series


    def __call__(self, element: Any) -> None:
        """Do the snapshots."""
        self._element = element


snapshot = SnapshotWithAssertions()
snapshot({"name": "John Doe", "age": 31})
snapshot.dict.assert_equal()

snapshot = SnapshotWithAssertions()
snapshot.list([1, 2, 3])
snapshot.list.has_same_length()

