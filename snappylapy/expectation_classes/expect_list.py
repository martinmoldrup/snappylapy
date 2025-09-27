"""Snapshot testing and expectations for lists."""
from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .base_snapshot import BaseSnapshot
from snappylapy.serialization import JsonPickleSerializer


class ListExpect(BaseSnapshot[list[Any]]):
    """Snapshot testing for lists."""

    serializer_class = JsonPickleSerializer[list[Any]]

    def __call__(
        self,
        data_to_snapshot: list[Any],
        name: str | None = None,
        filetype: str = "list.json",
    ) -> ListExpect:
        """Prepare a list for snapshot testing."""
        self._prepare_test(data_to_snapshot, name, filetype)
        return self

    def to_be(self, expected: list[Any]) -> None:
        """Assert that the list equals the expected list."""
        actual = self._ensure_data_available()
        assert actual == expected

    def to_equal(self, expected: list[Any]) -> None:
        """Deeply compare the list to the expected list."""
        actual = self._ensure_data_available()
        assert actual == expected

    def to_contain(self, item: Any) -> None:
        """Assert that the list contains the given item."""
        actual = self._ensure_data_available()
        if item not in actual:
            msg = f"Expected list to contain {item!r}"
            raise AssertionError(msg)

    def to_not_contain(self, item: Any) -> None:
        """Assert that the list does not contain the given item."""
        actual = self._ensure_data_available()
        if item in actual:
            msg = f"Expected list to not contain {item!r}"
            raise AssertionError(msg)

    def to_have_length(self, expected_length: int) -> None:
        """Assert that the list has the expected length."""
        actual = self._ensure_data_available()
        actual_length = len(actual)
        if actual_length != expected_length:
            msg = f"Expected list length {expected_length} but got {actual_length}"
            raise AssertionError(msg)

    def to_be_empty(self) -> None:
        """Assert that the list is empty."""
        actual = self._ensure_data_available()
        if actual:
            msg = "Expected list to be empty"
            raise AssertionError(msg)

    def to_not_be_empty(self) -> None:
        """Assert that the list is not empty."""
        actual = self._ensure_data_available()
        if not actual:
            msg = "Expected list to not be empty"
            raise AssertionError(msg)

    def to_contain_all_of(self, items: Iterable[Any]) -> None:
        """Assert that the list contains all of the given items."""
        actual = self._ensure_data_available()
        items_list = list(items)
        missing = [item for item in items_list if item not in actual]
        if missing:
            msg = f"Expected list to contain all items, missing: {missing!r}"
            raise AssertionError(msg)

    def to_contain_any_of(self, items: Iterable[Any]) -> None:
        """Assert that the list contains at least one of the given items."""
        actual = self._ensure_data_available()
        items_list = list(items)
        if not any(item in actual for item in items_list):
            msg = f"Expected list to contain at least one of {items_list!r}"
            raise AssertionError(msg)

    def to_start_with(self, prefix: list[Any]) -> None:
        """Assert that the list starts with the given prefix."""
        actual = self._ensure_data_available()
        if len(prefix) > len(actual):
            msg = f"Expected list to start with {prefix!r}, but list is too short"
            raise AssertionError(msg)
        if actual[:len(prefix)] != prefix:
            msg = f"Expected list to start with {prefix!r}"
            raise AssertionError(msg)

    def to_end_with(self, suffix: list[Any]) -> None:
        """Assert that the list ends with the given suffix."""
        actual = self._ensure_data_available()
        suffix_len = len(suffix)
        if suffix_len > len(actual):
            msg = f"Expected list to end with {suffix!r}, but list is too short"
            raise AssertionError(msg)
        if actual[-suffix_len:] != suffix:
            msg = f"Expected list to end with {suffix!r}"
            raise AssertionError(msg)

    def to_be_sorted(self, reverse: bool = False) -> None:
        """Assert that the list is sorted."""
        actual = self._ensure_data_available()
        sorted_list = sorted(actual, reverse=reverse)
        if actual != sorted_list:
            direction = "descending" if reverse else "ascending"
            msg = f"Expected list to be sorted in {direction} order"
            raise AssertionError(msg)

    def to_have_unique_elements(self) -> None:
        """Assert that all elements in the list are unique."""
        actual = self._ensure_data_available()
        if len(actual) != len(set(actual)):
            msg = "Expected all list elements to be unique"
            raise AssertionError(msg)

    def to_be_truthy(self) -> None:
        """Assert that the list evaluates to True."""
        actual = self._ensure_data_available()
        if not actual:
            msg = "Expected list to be truthy but it was falsy."
            raise AssertionError(msg)

    def to_be_falsy(self) -> None:
        """Assert that the list evaluates to False."""
        actual = self._ensure_data_available()
        if actual:
            msg = "Expected list to be falsy but it was truthy."
            raise AssertionError(msg)

    def _ensure_data_available(self) -> list[Any]:
        """Return the stored data ensuring it exists and is a list."""
        if self._data is None:
            msg = "No list data prepared yet. Call the expectation with data first."
            raise RuntimeError(msg)
        if not isinstance(self._data, list):
            msg = f"Expected list data but received {type(self._data).__name__}."
            raise TypeError(msg)
        return self._data
