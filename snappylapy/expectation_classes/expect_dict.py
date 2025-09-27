"""Snapshot testing and expectations for dicts."""

from __future__ import annotations

from .base_snapshot import BaseSnapshot
from collections.abc import Iterable, Mapping, Sequence
from copy import deepcopy
from numbers import Number
from snappylapy.serialization import JsonPickleSerializer
from typing import Any


class DictExpect(BaseSnapshot[dict]):
    """Snapshot testing for dictionaries."""

    serializer_class = JsonPickleSerializer[dict]

    def __call__(
        self,
        data_to_snapshot: dict,
        name: str | None = None,
        filetype: str = "dict.json",
    ) -> DictExpect:
        """Prepare a dictionary for snapshot testing."""
        self._ignored_keys: set[str] = set()
        self._original_data: dict = deepcopy(data_to_snapshot)
        self._prepare_test(data_to_snapshot, name, filetype)
        self._filtered_data: dict = self._current_data()
        return self

    def ignore_keys(self, keys: Iterable[str]) -> DictExpect:
        """Exclude the given keys from subsequent comparisons and snapshots."""
        if not hasattr(self, "_original_data"):
            msg = "No dictionary data prepared yet. Call the expectation with data first."
            raise RuntimeError(msg)
        if self._original_data is None:
            msg = "Cannot ignore keys when the dictionary value is None."
            raise TypeError(msg)
        self._ignored_keys = set(keys)
        self._filtered_data: dict = self._current_data()
        return self

    def to_be(self, expected: Mapping[str, Any]) -> None:
        """Assert that the dictionary equals the expected mapping."""
        actual = self._filtered_data
        expected_filtered = self._apply_ignored_keys(dict(expected))
        assert actual == expected_filtered

    def to_equal(self, expected: Mapping[str, Any]) -> None:
        """Deeply compare the dictionary to the expected mapping."""
        actual = self._filtered_data
        expected_filtered = self._apply_ignored_keys(dict(expected))
        assert actual == expected_filtered

    def to_be_close_to(self, expected: Mapping[str, Any], delta: float) -> None:
        """Assert that numeric values are within the provided delta and other values match exactly."""
        # TODO: Remove this method, as it does not seem useful for dicts.
        if delta < 0:
            msg = "Delta must be non-negative."
            raise ValueError(msg)
        actual = self._filtered_data
        expected_filtered = self._apply_ignored_keys(dict(expected))
        self._assert_close_value(actual, expected_filtered, delta, path=())

    def to_be_strictly_equal_to(self, expected: Mapping[str, Any]) -> None:
        """Assert that the dictionary matches by value and by exact value types."""
        actual = self._filtered_data
        expected_filtered = self._apply_ignored_keys(dict(expected))
        self._assert_strict_equality(actual, expected_filtered, path=())

    def to_have_the_same_properties_as_snapshot(self) -> None:
        """Assert that the dictionary has the same keys as the stored snapshot."""
        actual = self._filtered_data
        snapshot = self._get_deserialized_snapshot_data()
        snapshot_filtered = self._apply_ignored_keys(snapshot)
        actual_keys = set(actual.keys())
        expected_keys = set(snapshot_filtered.keys())
        if actual_keys != expected_keys:
            msg = f"Key mismatch: {sorted(actual_keys)!r} != {sorted(expected_keys)!r}"
            raise AssertionError(msg)

    def to_have_property(self, property_path: str) -> None:
        """Assert that the dictionary contains a property path (dot separated)."""
        data = self._filtered_data
        segments = [segment for segment in property_path.split(".") if segment]
        if not segments:
            msg = "Property path must not be empty."
            raise ValueError(msg)
        current: Any = data
        for segment in segments:
            if isinstance(current, Mapping) and segment in current:
                current = current[segment]
                continue
            msg = f"Property '{property_path}' not found."
            raise AssertionError(msg)

    def to_be_truthy(self) -> None:
        """Assert that the stored dictionary evaluates to True."""
        data = self._ensure_data_available()
        if not data:
            msg = "Expected value to be truthy but it was falsy."
            raise AssertionError(msg)

    def to_be_falsy(self) -> None:
        """Assert that the stored dictionary evaluates to False."""
        data = self._ensure_data_available()
        if data:
            msg = "Expected value to be falsy but it was truthy."
            raise AssertionError(msg)

    def _get_deserialized_snapshot_data(self) -> dict:
        """Read and deserialize snapshot data."""
        data_bin = self._read_snapshot_data()
        return self.serializer_class().deserialize(data_bin)

    def _get_deserialized_test_data(self) -> dict:
        """Read and deserialize test data."""
        data_bin = self._read_test_data()
        return self.serializer_class().deserialize(data_bin)

    def _apply_ignored_keys(self, data: dict) -> dict:
        """Return a new dictionary without ignored keys."""
        if data is None:
            return None
        if not getattr(self, "_ignored_keys", set()):
            return deepcopy(data)
        return {key: deepcopy(value) for key, value in data.items() if key not in self._ignored_keys}

    def _ensure_data_available(self) -> object:
        """Return the stored data ensuring it exists."""
        if self._data is None:
            msg = "No dictionary data prepared yet. Call the expectation with data first."
            raise RuntimeError(msg)
        return self._data

    def _current_data(self) -> dict[str, Any]:
        """Return the current dictionary data, ensuring the correct type."""
        data = self._ensure_data_available()
        if not isinstance(data, dict):
            msg = f"Expected dictionary data but received {type(data).__name__}."
            raise TypeError(msg)
        filtered_data = self._apply_ignored_keys(data)
        if filtered_data is None:
            msg = "Expected dictionary data but received None."
            raise TypeError(msg)
        return filtered_data

    def _assert_close_value(
        self,
        actual: object,
        expected: object,
        delta: float,
        path: tuple[str, ...],
    ) -> None:
        """
        Assert that values are close within the provided delta.

        delta is a 
        """
        if isinstance(actual, Mapping) and isinstance(expected, Mapping):
            self._assert_close_mapping(actual, expected, delta, path)
            return
        if (
            isinstance(actual, Sequence)
            and isinstance(expected, Sequence)
            and not isinstance(actual, (str, bytes, bytearray))
        ):
            if len(actual) != len(expected):
                joined_path = "".join(path)
                msg = f"Sequence length mismatch at {joined_path}: {len(actual)} != {len(expected)}"
                raise AssertionError(msg)
            for index, (actual_item, expected_item) in enumerate(zip(actual, expected)):
                self._assert_close_value(actual_item, expected_item, delta, (*path, f"[{index}]"))
            return
        if isinstance(actual, bool) or isinstance(expected, bool):
            if actual != expected:
                joined_path = "".join(path)
                msg = f"Boolean mismatch at {joined_path}: {actual!r} != {expected!r}"
                raise AssertionError(msg)
            return
        if isinstance(actual, Number) and isinstance(expected, Number):
            if abs(float(actual) - float(expected)) > delta:
                joined_path = "".join(path)
                msg = f"Numeric mismatch at {joined_path}: {actual!r} is not within {delta} of {expected!r}."
                raise AssertionError(msg)
            return
        if actual != expected:
            joined_path = "".join(path)
            msg = f"Value mismatch at {joined_path}: {actual!r} != {expected!r}"
            raise AssertionError(msg)

    def _assert_close_mapping(
        self,
        actual: Mapping[str, Any],
        expected: Mapping[str, Any],
        delta: float,
        path: tuple[str, ...],
    ) -> None:
        """Assert that two mappings are close within delta."""
        actual_keys = set(actual.keys())
        expected_keys = set(expected.keys())
        if actual_keys != expected_keys:
            joined_path = "".join(path)
            msg = f"Key mismatch at {joined_path}: {sorted(actual_keys)!r} != {sorted(expected_keys)!r}"
            raise AssertionError(msg)
        for key in actual_keys:
            self._assert_close_value(actual[key], expected[key], delta, (*path, f".{key}"))

    def _assert_strict_equality(self, actual: object, expected: object, path: tuple[str, ...]) -> None:
        """Assert that two values are strictly equal, including their types."""
        if type(actual) is not type(expected):
            joined_path = "".join(path)
            msg = f"Type mismatch at {joined_path}: {type(actual).__name__} != {type(expected).__name__}"
            raise AssertionError(msg)
        if isinstance(actual, Mapping) and isinstance(expected, Mapping):
            actual_keys = set(actual.keys())
            expected_keys = set(expected.keys())
            if actual_keys != expected_keys:
                joined_path = "".join(path)
                msg = f"Key mismatch at {joined_path}: {sorted(actual_keys)!r} != {sorted(expected_keys)!r}"
                raise AssertionError(msg)
            for key in actual_keys:
                self._assert_strict_equality(actual[key], expected[key], (*path, f".{key}"))
            return
        if (
            isinstance(actual, Sequence)
            and isinstance(expected, Sequence)
            and not isinstance(actual, (str, bytes, bytearray))
        ):
            if len(actual) != len(expected):
                joined_path = "".join(path)
                msg = f"Sequence length mismatch at {joined_path}: {len(actual)} != {len(expected)}"
                raise AssertionError(msg)
            for index, (actual_item, expected_item) in enumerate(zip(actual, expected)):
                self._assert_strict_equality(actual_item, expected_item, (*path, f"[{index}]"))
            return
        if actual != expected:
            joined_path = "".join(path)
            msg = f"Value mismatch at {joined_path}: {actual!r} != {expected!r}"
            raise AssertionError(msg)
