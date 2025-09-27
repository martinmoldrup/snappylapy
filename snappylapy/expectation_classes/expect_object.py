"""Snapshot testing and expectations for generic custom objects."""
from __future__ import annotations

from collections.abc import Iterable

from .base_snapshot import BaseSnapshot
from snappylapy.serialization import JsonPickleSerializer


class ObjectExpect(BaseSnapshot[object]):
    """Snapshot testing for generic objects."""

    serializer_class = JsonPickleSerializer[object]

    def __call__(
        self,
        data_to_snapshot: object,
        name: str | None = None,
        filetype: str = "object.json",
    ) -> ObjectExpect:
        """Prepare an object for snapshot testing."""
        self._prepare_test(data_to_snapshot, name, filetype)
        self._data_prepared = True
        return self

    def to_be(self, expected: object) -> None:
        """Assert that the object equals the expected object."""
        actual = self._ensure_data_available()
        assert actual == expected

    def to_equal(self, expected: object) -> None:
        """Deeply compare the object to the expected object."""
        actual = self._ensure_data_available()
        assert actual == expected

    def to_be_strictly_equal_to(self, expected: object) -> None:
        """Assert that the object matches by value and by exact type."""
        actual = self._ensure_data_available()
        if type(actual) is not type(expected):
            msg = f"Type mismatch: {type(actual).__name__} != {type(expected).__name__}"
            raise AssertionError(msg)
        assert actual == expected

    def to_be_truthy(self) -> None:
        """Assert that the stored object evaluates to True."""
        data = self._ensure_data_available()
        if not data:
            msg = "Expected value to be truthy but it was falsy."
            raise AssertionError(msg)

    def to_be_falsy(self) -> None:
        """Assert that the stored object evaluates to False."""
        data = self._ensure_data_available()
        if data:
            msg = "Expected value to be falsy but it was truthy."
            raise AssertionError(msg)

    def to_be_instance_of(self, expected_type: type) -> None:
        """Assert that the object is an instance of the expected type."""
        actual = self._ensure_data_available()
        if not isinstance(actual, expected_type):
            msg = f"Expected instance of {expected_type.__name__} but got {type(actual).__name__}"
            raise TypeError(msg)

    def to_have_attribute(self, attribute_name: str) -> None:
        """Assert that the object has the specified attribute."""
        actual = self._ensure_data_available()
        if not hasattr(actual, attribute_name):
            msg = f"Object does not have attribute '{attribute_name}'"
            raise AssertionError(msg)

    def to_have_attributes(self, attribute_names: Iterable[str]) -> None:
        """Assert that the object has all the specified attributes."""
        actual = self._ensure_data_available()
        missing_attributes = [name for name in attribute_names if not hasattr(actual, name)]
        if missing_attributes:
            msg = f"Object is missing attributes: {missing_attributes}"
            raise AssertionError(msg)

    def to_be_none(self) -> None:
        """Assert that the object is None."""
        actual = self._ensure_data_available()
        if actual is not None:
            msg = f"Expected None but got {type(actual).__name__}"
            raise AssertionError(msg)

    def to_not_be_none(self) -> None:
        """Assert that the object is not None."""
        actual = self._ensure_data_available()
        if actual is None:
            msg = "Expected value to not be None"
            raise AssertionError(msg)

    def _ensure_data_available(self) -> object:
        """Return the stored data ensuring it exists."""
        if not getattr(self, "_data_prepared", False):
            msg = "No object data prepared yet. Call the expectation with data first."
            raise RuntimeError(msg)
        return self._data
