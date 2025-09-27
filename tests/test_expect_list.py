"""Tests for the list expectation helper."""
from __future__ import annotations

import pathlib
from typing import Any

import pytest

from snappylapy.expectation_classes.expect_list import ListExpect
from snappylapy.models import Settings
from snappylapy.session import SnapshotSession


@pytest.fixture
def list_expect(tmp_path: pathlib.Path) -> ListExpect:
    """Provide a ListExpect instance with temporary snapshot directories."""
    settings = Settings(
        test_filename="test_expect_list",
        test_function="test_case",
        snapshots_base_dir=tmp_path,
    )
    return ListExpect(settings=settings, snappylapy_session=SnapshotSession())


def test_to_be_success(list_expect: ListExpect) -> None:
    """The to_be assertion should pass on identical lists."""
    payload = [1, 2, 3]
    list_expect(payload).to_be([1, 2, 3])


def test_to_be_failure(list_expect: ListExpect) -> None:
    """The to_be assertion should fail on different lists."""
    payload = [1, 2, 3]
    with pytest.raises(AssertionError):
        list_expect(payload).to_be([1, 2, 4])


def test_to_contain_success(list_expect: ListExpect) -> None:
    """The to_contain assertion should pass when item is present."""
    list_expect([1, 2, 3]).to_contain(2)
    list_expect(["a", "b", "c"]).to_contain("b")


def test_to_contain_failure(list_expect: ListExpect) -> None:
    """The to_contain assertion should fail when item is not present."""
    with pytest.raises(AssertionError, match="Expected list to contain 4"):
        list_expect([1, 2, 3]).to_contain(4)


def test_to_not_contain_success(list_expect: ListExpect) -> None:
    """The to_not_contain assertion should pass when item is not present."""
    list_expect([1, 2, 3]).to_not_contain(4)


def test_to_not_contain_failure(list_expect: ListExpect) -> None:
    """The to_not_contain assertion should fail when item is present."""
    with pytest.raises(AssertionError, match="Expected list to not contain 2"):
        list_expect([1, 2, 3]).to_not_contain(2)


def test_to_have_length_success(list_expect: ListExpect) -> None:
    """The to_have_length assertion should pass for correct length."""
    list_expect([1, 2, 3]).to_have_length(3)


def test_to_have_length_failure(list_expect: ListExpect) -> None:
    """The to_have_length assertion should fail for incorrect length."""
    with pytest.raises(AssertionError, match="Expected list length 5 but got 3"):
        list_expect([1, 2, 3]).to_have_length(5)


def test_to_be_empty_success(list_expect: ListExpect) -> None:
    """The to_be_empty assertion should pass for empty lists."""
    list_expect([]).to_be_empty()


def test_to_be_empty_failure(list_expect: ListExpect) -> None:
    """The to_be_empty assertion should fail for non-empty lists."""
    with pytest.raises(AssertionError, match="Expected list to be empty"):
        list_expect([1, 2, 3]).to_be_empty()


def test_to_not_be_empty_success(list_expect: ListExpect) -> None:
    """The to_not_be_empty assertion should pass for non-empty lists."""
    list_expect([1, 2, 3]).to_not_be_empty()


def test_to_not_be_empty_failure(list_expect: ListExpect) -> None:
    """The to_not_be_empty assertion should fail for empty lists."""
    with pytest.raises(AssertionError, match="Expected list to not be empty"):
        list_expect([]).to_not_be_empty()


def test_to_contain_all_of_success(list_expect: ListExpect) -> None:
    """The to_contain_all_of assertion should pass when all items are present."""
    list_expect([1, 2, 3, 4, 5]).to_contain_all_of([2, 4])


def test_to_contain_all_of_failure(list_expect: ListExpect) -> None:
    """The to_contain_all_of assertion should fail when some items are missing."""
    with pytest.raises(AssertionError, match="Expected list to contain all items, missing:"):
        list_expect([1, 2, 3]).to_contain_all_of([2, 4, 6])


def test_to_contain_any_of_success(list_expect: ListExpect) -> None:
    """The to_contain_any_of assertion should pass when any item is present."""
    list_expect([1, 2, 3]).to_contain_any_of([4, 5, 2])


def test_to_contain_any_of_failure(list_expect: ListExpect) -> None:
    """The to_contain_any_of assertion should fail when no item is present."""
    with pytest.raises(AssertionError, match="Expected list to contain at least one of"):
        list_expect([1, 2, 3]).to_contain_any_of([4, 5, 6])


def test_to_start_with_success(list_expect: ListExpect) -> None:
    """The to_start_with assertion should pass when list starts with prefix."""
    list_expect([1, 2, 3, 4, 5]).to_start_with([1, 2])


def test_to_start_with_failure(list_expect: ListExpect) -> None:
    """The to_start_with assertion should fail when list doesn't start with prefix."""
    with pytest.raises(AssertionError, match="Expected list to start with"):
        list_expect([1, 2, 3, 4, 5]).to_start_with([2, 3])


def test_to_start_with_too_long(list_expect: ListExpect) -> None:
    """The to_start_with assertion should fail when prefix is longer than list."""
    with pytest.raises(AssertionError, match="Expected list to start with .*, but list is too short"):
        list_expect([1, 2]).to_start_with([1, 2, 3, 4])


def test_to_end_with_success(list_expect: ListExpect) -> None:
    """The to_end_with assertion should pass when list ends with suffix."""
    list_expect([1, 2, 3, 4, 5]).to_end_with([4, 5])


def test_to_end_with_failure(list_expect: ListExpect) -> None:
    """The to_end_with assertion should fail when list doesn't end with suffix."""
    with pytest.raises(AssertionError, match="Expected list to end with"):
        list_expect([1, 2, 3, 4, 5]).to_end_with([3, 4])


def test_to_end_with_too_long(list_expect: ListExpect) -> None:
    """The to_end_with assertion should fail when suffix is longer than list."""
    with pytest.raises(AssertionError, match="Expected list to end with .*, but list is too short"):
        list_expect([1, 2]).to_end_with([1, 2, 3, 4])


def test_to_be_sorted_ascending_success(list_expect: ListExpect) -> None:
    """The to_be_sorted assertion should pass for ascending sorted lists."""
    list_expect([1, 2, 3, 4, 5]).to_be_sorted()
    list_expect(["a", "b", "c"]).to_be_sorted()


def test_to_be_sorted_ascending_failure(list_expect: ListExpect) -> None:
    """The to_be_sorted assertion should fail for unsorted lists."""
    with pytest.raises(AssertionError, match="Expected list to be sorted in ascending order"):
        list_expect([3, 1, 2]).to_be_sorted()


def test_to_be_sorted_descending_success(list_expect: ListExpect) -> None:
    """The to_be_sorted assertion should pass for descending sorted lists."""
    list_expect([5, 4, 3, 2, 1]).to_be_sorted(reverse=True)


def test_to_be_sorted_descending_failure(list_expect: ListExpect) -> None:
    """The to_be_sorted assertion should fail for incorrectly sorted lists."""
    with pytest.raises(AssertionError, match="Expected list to be sorted in descending order"):
        list_expect([1, 2, 3]).to_be_sorted(reverse=True)


def test_to_have_unique_elements_success(list_expect: ListExpect) -> None:
    """The to_have_unique_elements assertion should pass for lists with unique elements."""
    list_expect([1, 2, 3, 4, 5]).to_have_unique_elements()


def test_to_have_unique_elements_failure(list_expect: ListExpect) -> None:
    """The to_have_unique_elements assertion should fail for lists with duplicates."""
    with pytest.raises(AssertionError, match="Expected all list elements to be unique"):
        list_expect([1, 2, 3, 2, 4]).to_have_unique_elements()


def test_to_be_truthy_success(list_expect: ListExpect) -> None:
    """The to_be_truthy assertion should pass for non-empty lists."""
    list_expect([1, 2, 3]).to_be_truthy()


def test_to_be_truthy_failure(list_expect: ListExpect) -> None:
    """The to_be_truthy assertion should fail for empty lists."""
    with pytest.raises(AssertionError, match="Expected list to be truthy"):
        list_expect([]).to_be_truthy()


def test_to_be_falsy_success(list_expect: ListExpect) -> None:
    """The to_be_falsy assertion should pass for empty lists."""
    list_expect([]).to_be_falsy()


def test_to_be_falsy_failure(list_expect: ListExpect) -> None:
    """The to_be_falsy assertion should fail for non-empty lists."""
    with pytest.raises(AssertionError, match="Expected list to be falsy"):
        list_expect([1, 2, 3]).to_be_falsy()


def test_ensure_data_available_no_data(list_expect: ListExpect) -> None:
    """The _ensure_data_available method should raise when no data is prepared."""
    with pytest.raises(RuntimeError, match="No list data prepared yet"):
        list_expect.to_be_truthy()


def test_ensure_data_available_wrong_type(list_expect: ListExpect) -> None:
    """The _ensure_data_available method should raise when data is not a list."""
    list_expect._data = "not a list"  # Force wrong type  # noqa: SLF001
    with pytest.raises(TypeError, match="Expected list data but received str"):
        list_expect.to_be_truthy()