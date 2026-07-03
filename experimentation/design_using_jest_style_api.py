"""Jest style testing, this is a design document, only for exploration purposes, only a suggestion."""
import pytest
from typing import Any

class DictClass:

    def __init__(self):
        self._ignored_keys = []

    def __call__(self, element: Any) -> "DictClass":
        self.element = element
        return self
    
    def ignore_keys(self, keys: list[str]) -> "DictClass":
        """Ignores the keys from the snapshot."""
        self._ignored_keys = keys

    def to_match_snapshot(self):
        """Asserts that the element matches the snapshot."""
        pass

    def to_be(expected: dict):
        """Asserts that the element is equal to the expected dictionary."""
        # With jestspectation functions
        pass

    def to_be_close_to(expected: dict, delta: float):
        """Asserts that the element is close to the expected dictionary."""

    def to_equal(expected: dict):
        """Deeply compares the element with the expected dictionary."""

    def to_be_scrictly_equal_to(expected: dict):
        """Asserts that the element is strictly equal to the expected dictionary."""

    def to_have_property(property_name: str):
        """Asserts that the element has the property."""

    def to_thow_error():
        """Asserts that the element throws an error."""

    def to_be_none():
        """Asserts that the element is None."""

    def to_be_truthy():
        """Asserts that the element is truthy."""

    def to_be_falsy():
        """Asserts that the element is falsy."""

    def to_be_defined():
        """Asserts that the element is defined."""

class StringClass:
    def __init__(self):
        pass

    def __call__(self, element: str) -> "StringClass":
        self.element = element
        return self

    def to_match_snapshot(self):
        pass

    def to_be(expected: str):
        pass

    def to_be_close_to(expected: str, delta: float):
        pass

    def to_equal(expected: str):
        pass

    def to_be_scrictly_equal_to(expected: str):
        pass

    def to_have_property(property_name: str):
        pass

    def to_thow_error():
        pass

    def to_be_none():
        pass

    def to_be_truthy():
        pass

    def to_be_falsy():
        pass

    def to_be_defined():
        pass

class Expect:
    def __init__(self):
        self.dict = DictClass()
        self.string = StringClass()





def test_do_simple_snapshot(expect: Expect):
    expect.dict({
        "name": "John Doe",
        "age": 31
    }).to_match_snapshot()

def test_do_simple_snapshot_with_ignored_keys(expect: Expect):
    expect.dict({
        "name": "John Doe",
        "age": 31,
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "state": "AS",
            "zip": "12345"
        }
    }).ignore_keys(["address"]).to_match_snapshot()

def test_do_string_snapshot(expect: Expect):
    expect.string("Hello World").to_match_snapshot()
