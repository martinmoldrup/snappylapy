"""Snapshot testing and expectations for strings."""
from __future__ import annotations

import re
from .base_snapshot import BaseSnapshot
from collections.abc import Iterable
from difflib import SequenceMatcher
from snappylapy.serialization import StringSerializer
from typing_extensions import Self


class StringExpect(BaseSnapshot[str]):  # noqa: PLR0904 - many assertion helpers are intentional
    """Snapshot testing for strings."""

    serializer_class = StringSerializer

    def __call__(self,
                 data_to_snapshot: str,
                 name: str | None = None,
                 filetype: str = "string.txt") -> StringExpect:
        """Prepare a string for snapshot testing."""
        self._prepare_test(data_to_snapshot, name, filetype)
        return self

    def to_be(self, expected: str) -> Self:
        """Assert that the string equals the expected string."""
        actual = self._ensure_data_available()
        assert actual == expected
        return self

    def to_equal(self, expected: str) -> Self:
        """Assert that the string equals the expected string (alias)."""
        actual = self._ensure_data_available()
        assert actual == expected
        return self

    def to_contain(self, substring: str) -> Self:
        """Assert that the string contains the given substring."""
        actual = self._ensure_data_available()
        if substring not in actual:
            msg = f"Expected string to contain '{substring}'"
            raise AssertionError(msg)
        return self

    def to_not_contain(self, substring: str) -> Self:
        """Assert that the string does not contain the given substring."""
        actual = self._ensure_data_available()
        if substring in actual:
            msg = f"Expected string to not contain '{substring}'"
            raise AssertionError(msg)
        return self

    def to_start_with(self, prefix: str) -> Self:
        """Assert that the string starts with the given prefix."""
        actual = self._ensure_data_available()
        if not actual.startswith(prefix):
            msg = f"Expected string to start with '{prefix}'"
            raise AssertionError(msg)
        return self

    def to_end_with(self, suffix: str) -> Self:
        """Assert that the string ends with the given suffix."""
        actual = self._ensure_data_available()
        if not actual.endswith(suffix):
            msg = f"Expected string to end with '{suffix}'"
            raise AssertionError(msg)
        return self

    def to_have_length(self, expected_length: int) -> Self:
        """Assert that the string has the expected length."""
        actual = self._ensure_data_available()
        actual_length = len(actual)
        if actual_length != expected_length:
            msg = f"Expected string length {expected_length} but got {actual_length}"
            raise AssertionError(msg)
        return self

    def to_be_empty(self) -> Self:
        """Assert that the string is empty."""
        actual = self._ensure_data_available()
        if actual:
            msg = "Expected string to be empty"
            raise AssertionError(msg)
        return self

    def to_not_be_empty(self) -> Self:
        """Assert that the string is not empty."""
        actual = self._ensure_data_available()
        if not actual:
            msg = "Expected string to not be empty"
            raise AssertionError(msg)
        return self

    def to_match_regex(self, pattern: str, flags: int = 0) -> Self:
        """Assert that the string matches the given regex pattern."""
        actual = self._ensure_data_available()
        if not re.search(pattern, actual, flags):
            msg = f"Expected string to match regex pattern '{pattern}'"
            raise AssertionError(msg)
        return self

    def to_not_match_regex(self, pattern: str, flags: int = 0) -> Self:
        """Assert that the string does not match the given regex pattern."""
        actual = self._ensure_data_available()
        if re.search(pattern, actual, flags):
            msg = f"Expected string to not match regex pattern '{pattern}'"
            raise AssertionError(msg)
        return self

    def to_be_uppercase(self) -> Self:
        """Assert that the string is uppercase."""
        actual = self._ensure_data_available()
        if not actual.isupper():
            msg = "Expected string to be uppercase"
            raise AssertionError(msg)
        return self

    def to_be_lowercase(self) -> Self:
        """Assert that the string is lowercase."""
        actual = self._ensure_data_available()
        if not actual.islower():
            msg = "Expected string to be lowercase"
            raise AssertionError(msg)
        return self

    def to_be_title_case(self) -> Self:
        """Assert that the string is in title case."""
        actual = self._ensure_data_available()
        if not actual.istitle():
            msg = "Expected string to be in title case"
            raise AssertionError(msg)
        return self

    def to_be_numeric(self) -> Self:
        """Assert that the string represents a numeric value."""
        actual = self._ensure_data_available()
        if not actual.isnumeric():
            msg = "Expected string to be numeric"
            raise AssertionError(msg)
        return self

    def to_be_alphabetic(self) -> Self:
        """Assert that the string contains only alphabetic characters."""
        actual = self._ensure_data_available()
        if not actual.isalpha():
            msg = "Expected string to be alphabetic"
            raise AssertionError(msg)
        return self

    def to_be_alphanumeric(self) -> Self:
        """Assert that the string contains only alphanumeric characters."""
        actual = self._ensure_data_available()
        if not actual.isalnum():
            msg = "Expected string to be alphanumeric"
            raise AssertionError(msg)
        return self

    def to_contain_any_of(self, substrings: Iterable[str]) -> Self:
        """Assert that the string contains at least one of the given substrings."""
        actual = self._ensure_data_available()
        substring_list = list(substrings)
        if not any(substring in actual for substring in substring_list):
            msg = f"Expected string to contain at least one of {substring_list}"
            raise AssertionError(msg)
        return self

    def to_contain_all_of(self, substrings: Iterable[str]) -> Self:
        """Assert that the string contains all of the given substrings."""
        actual = self._ensure_data_available()
        substring_list = list(substrings)
        missing = [substring for substring in substring_list if substring not in actual]
        if missing:
            msg = f"Expected string to contain all substrings, missing: {missing}"
            raise AssertionError(msg)
        return self

    def to_fuzzy_match(self, expected: str, similarity: float = 0.8) -> Self:
        """Assert that the string is similar to expected string within similarity threshold."""
        actual = self._ensure_data_available()
        matcher = SequenceMatcher(None, actual, expected)
        actual_similarity = matcher.ratio()
        if actual_similarity < similarity:
            msg = f"Expected similarity >= {similarity}, but got {actual_similarity:.2f}"
            raise AssertionError(msg)
        return self

    def to_be_truthy(self) -> Self:
        """Assert that the string evaluates to True."""
        actual = self._ensure_data_available()
        if not actual:
            msg = "Expected string to be truthy but it was falsy."
            raise AssertionError(msg)
        return self

    def to_be_falsy(self) -> Self:
        """Assert that the string evaluates to False."""
        actual = self._ensure_data_available()
        if actual:
            msg = "Expected string to be falsy but it was truthy."
            raise AssertionError(msg)
        return self

    def _ensure_data_available(self) -> str:
        """Return the stored data ensuring it exists and is a string."""
        if self._data is None:
            msg = "No string data prepared yet. Call the expectation with data first."
            raise RuntimeError(msg)
        if not isinstance(self._data, str):
            msg = f"Expected string data but received {type(self._data).__name__}."
            raise TypeError(msg)
        return self._data
