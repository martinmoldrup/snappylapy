"""Tests for the object expectation helper."""
from __future__ import annotations

import pathlib
from dataclasses import dataclass

import pytest

from snappylapy.expectation_classes.expect_object import ObjectExpect
from snappylapy.models import Settings
from snappylapy.session import SnapshotSession


@dataclass
class SampleClass:
    """Sample class for testing."""
    
    name: str
    value: int


@pytest.fixture
def object_expect(tmp_path: pathlib.Path) -> ObjectExpect:
    """Provide an ObjectExpect instance with temporary snapshot directories."""
    settings = Settings(
        test_filename="test_expect_object",
        test_function="test_case",
        snapshots_base_dir=tmp_path,
    )
    return ObjectExpect(settings=settings, snappylapy_session=SnapshotSession())


def test_to_be_success(object_expect: ObjectExpect) -> None:
    """The to_be assertion should pass on identical objects."""
    payload = SampleClass("Alice", 30)
    object_expect(payload).to_be(SampleClass("Alice", 30))


def test_to_be_raises_on_difference(object_expect: ObjectExpect) -> None:
    """The to_be assertion should raise when objects differ."""
    payload = SampleClass("Alice", 30)
    with pytest.raises(AssertionError):
        object_expect(payload).to_be(SampleClass("Alice", 29))


def test_to_equal_success(object_expect: ObjectExpect) -> None:
    """The to_equal assertion should pass on identical objects."""
    payload = {"key": "value"}
    object_expect(payload).to_equal({"key": "value"})


def test_to_equal_raises_on_difference(object_expect: ObjectExpect) -> None:
    """The to_equal assertion should raise when objects differ."""
    payload = {"key": "value"}
    with pytest.raises(AssertionError):
        object_expect(payload).to_equal({"key": "different"})


def test_to_be_strictly_equal_to_success(object_expect: ObjectExpect) -> None:
    """The to_be_strictly_equal_to assertion should pass on identical types and values."""
    payload = 42
    object_expect(payload).to_be_strictly_equal_to(42)


def test_to_be_strictly_equal_to_type_mismatch(object_expect: ObjectExpect) -> None:
    """The to_be_strictly_equal_to assertion should raise on type mismatch."""
    payload = 42
    with pytest.raises(AssertionError, match="Type mismatch"):
        object_expect(payload).to_be_strictly_equal_to(42.0)


def test_to_be_truthy_success(object_expect: ObjectExpect) -> None:
    """The to_be_truthy assertion should pass on truthy objects."""
    object_expect("non-empty string").to_be_truthy()
    object_expect([1, 2, 3]).to_be_truthy()
    object_expect({"key": "value"}).to_be_truthy()


def test_to_be_truthy_failure(object_expect: ObjectExpect) -> None:
    """The to_be_truthy assertion should fail on falsy objects."""
    with pytest.raises(AssertionError, match="Expected value to be truthy"):
        object_expect("").to_be_truthy()
    with pytest.raises(AssertionError, match="Expected value to be truthy"):
        object_expect([]).to_be_truthy()
    with pytest.raises(AssertionError, match="Expected value to be truthy"):
        object_expect({}).to_be_truthy()


def test_to_be_falsy_success(object_expect: ObjectExpect) -> None:
    """The to_be_falsy assertion should pass on falsy objects."""
    object_expect("").to_be_falsy()
    object_expect([]).to_be_falsy()
    object_expect({}).to_be_falsy()
    object_expect(0).to_be_falsy()
    object_expect(False).to_be_falsy()


def test_to_be_falsy_failure(object_expect: ObjectExpect) -> None:
    """The to_be_falsy assertion should fail on truthy objects."""
    with pytest.raises(AssertionError, match="Expected value to be falsy"):
        object_expect("non-empty").to_be_falsy()


def test_to_be_instance_of_success(object_expect: ObjectExpect) -> None:
    """The to_be_instance_of assertion should pass for correct types."""
    object_expect("test").to_be_instance_of(str)
    object_expect([1, 2, 3]).to_be_instance_of(list)


def test_to_be_instance_of_failure(object_expect: ObjectExpect) -> None:
    """The to_be_instance_of assertion should fail for incorrect types."""
    with pytest.raises(TypeError, match="Expected instance of int but got str"):
        object_expect("test").to_be_instance_of(int)


def test_to_have_attribute_success(object_expect: ObjectExpect) -> None:
    """The to_have_attribute assertion should pass for existing attributes."""
    payload = SampleClass("Alice", 30)
    object_expect(payload).to_have_attribute("name")
    object_expect(payload).to_have_attribute("value")


def test_to_have_attribute_failure(object_expect: ObjectExpect) -> None:
    """The to_have_attribute assertion should fail for missing attributes."""
    payload = SampleClass("Alice", 30)
    with pytest.raises(AssertionError, match="Object does not have attribute 'missing'"):
        object_expect(payload).to_have_attribute("missing")


def test_to_have_attributes_success(object_expect: ObjectExpect) -> None:
    """The to_have_attributes assertion should pass when all attributes exist."""
    payload = SampleClass("Alice", 30)
    object_expect(payload).to_have_attributes(["name", "value"])


def test_to_have_attributes_failure(object_expect: ObjectExpect) -> None:
    """The to_have_attributes assertion should fail when attributes are missing."""
    payload = SampleClass("Alice", 30)
    with pytest.raises(AssertionError, match="Object is missing attributes"):
        object_expect(payload).to_have_attributes(["name", "missing", "also_missing"])


def test_to_be_none_success(object_expect: ObjectExpect) -> None:
    """The to_be_none assertion should pass for None values."""
    object_expect(None).to_be_none()


def test_to_be_none_failure(object_expect: ObjectExpect) -> None:
    """The to_be_none assertion should fail for non-None values."""
    with pytest.raises(AssertionError, match="Expected None but got str"):
        object_expect("not none").to_be_none()


def test_to_not_be_none_success(object_expect: ObjectExpect) -> None:
    """The to_not_be_none assertion should pass for non-None values."""
    object_expect("not none").to_not_be_none()
    object_expect(0).to_not_be_none()
    object_expect([]).to_not_be_none()


def test_to_not_be_none_failure(object_expect: ObjectExpect) -> None:
    """The to_not_be_none assertion should fail for None values."""
    with pytest.raises(AssertionError, match="Expected value to not be None"):
        object_expect(None).to_not_be_none()


def test_ensure_data_available_no_data(object_expect: ObjectExpect) -> None:
    """The _ensure_data_available method should raise when no data is prepared."""
    with pytest.raises(RuntimeError, match="No object data prepared yet"):
        object_expect.to_be_truthy()