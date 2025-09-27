"""Tests for the dictionary expectation helper."""
from __future__ import annotations

import pytest
import pathlib
from snappylapy.expectation_classes.expect_dict import DictExpect
from snappylapy.models import Settings
from snappylapy.session import SnapshotSession


@pytest.fixture
def dict_expect(tmp_path: pathlib.Path) -> DictExpect:
    """Provide a DictExpect instance with temporary snapshot directories."""
    settings = Settings(
        test_filename="test_expect_dict",
        test_function="test_case",
        snapshots_base_dir=tmp_path,
    )
    return DictExpect(settings=settings, snappylapy_session=SnapshotSession())


def test_to_be_success(dict_expect: DictExpect) -> None:
    """The to_be assertion should pass on identical dictionaries."""
    payload = {"name": "Alice", "age": 30}
    dict_expect(payload).to_be({"name": "Alice", "age": 30})


def test_to_be_raises_on_difference(dict_expect: DictExpect) -> None:
    """The to_be assertion should raise when dictionaries differ."""
    payload = {"name": "Alice", "age": 30}
    with pytest.raises(AssertionError):
        dict_expect(payload).to_be({"name": "Alice", "age": 29})


def test_ignore_keys_does_not_persist_filtered_data(
    dict_expect: DictExpect, tmp_path: pathlib.Path,
) -> None:
    """Ignoring keys should skip persistence changes but affect runtime comparisons."""
    payload = {"keep": 1, "drop": 2}
    expectation = dict_expect(payload).ignore_keys(["drop"])
    expectation.to_equal({"keep": 1})
    stored_path = tmp_path / "__test_results__" / expectation.settings.filename
    stored = expectation.serializer_class().deserialize(stored_path.read_bytes())
    assert stored == payload

    expectation.settings.snapshot_update = True
    expectation.to_match_snapshot()
    snapshot_path = tmp_path / "__snapshots__" / expectation.settings.filename
    snapshot = expectation.serializer_class().deserialize(snapshot_path.read_bytes())
    assert snapshot == payload


def test_to_be_close_to(dict_expect: DictExpect) -> None:
    """to_be_close_to should allow small numeric differences."""
    payload = {"lat": 12.0, "nested": {"value": 20.0}}
    expectation = dict_expect(payload)
    expectation.to_be_close_to({"lat": 12.05, "nested": {"value": 19.95}}, delta=0.1)
    with pytest.raises(AssertionError):
        expectation.to_be_close_to({"lat": 12.5, "nested": {"value": 19.95}}, delta=0.1)


def test_to_be_strictly_equal_to_types(dict_expect: DictExpect) -> None:
    """to_be_strictly_equal_to should fail when value types differ."""
    payload = {"total": 5, "items": [1, 2, 3]}
    expectation = dict_expect(payload)
    expectation.to_be_strictly_equal_to({"total": 5, "items": [1, 2, 3]})
    with pytest.raises(AssertionError):
        expectation.to_be_strictly_equal_to({"total": 5.0, "items": [1, 2, 3]})


def test_to_have_property_nested(dict_expect: DictExpect) -> None:
    """Nested properties should be discoverable."""
    payload = {"address": {"city": "Copenhagen", "zip": "2100"}}
    expectation = dict_expect(payload)
    expectation.to_have_property("address.city")
    with pytest.raises(AssertionError):
        expectation.to_have_property("address.country")


def test_to_be_truthy(dict_expect: DictExpect) -> None:
    """Truthiness assertions should reflect boolean evaluation of the payload."""
    dict_expect({"active": True}).to_be_truthy()
    with pytest.raises(AssertionError):
        dict_expect({}).to_be_truthy()

def test_to_be_falsy(dict_expect: DictExpect) -> None:
    """Falsiness assertions should reflect boolean evaluation of the payload."""
    dict_expect({}).to_be_falsy()
    with pytest.raises(AssertionError):
        dict_expect({"value": 0}).to_be_falsy()

def test_to_have_the_same_properties_as_snapshot_success(
    dict_expect: DictExpect
) -> None:
    """to_have_the_same_properties_as_snapshot should compare keys only."""
    dict_expect.settings.snapshot_update = True
    payload = {"name": "Alice", "age": 30}
    expectation = dict_expect(payload)
    expectation.to_match_snapshot()

    # Same keys, different values - should pass
    dict_expect({"name": "Bob", "age": 25}).to_have_the_same_properties_as_snapshot()

def test_to_have_the_same_properties_as_snapshot_failure(
    dict_expect: DictExpect
) -> None:
    """to_have_the_same_properties_as_snapshot should raise on key differences."""
    dict_expect.settings.snapshot_update = True
    payload = {"name": "Alice", "age": 30}
    expectation = dict_expect(payload)
    expectation.to_match_snapshot()
    # Different keys - should fail
    with pytest.raises(AssertionError):
        dict_expect({"name": "Alice", "age": 30, "city": "Wonderland"}).to_have_the_same_properties_as_snapshot()
    with pytest.raises(AssertionError):
        dict_expect({"name": "Alice"}).to_have_the_same_properties_as_snapshot()