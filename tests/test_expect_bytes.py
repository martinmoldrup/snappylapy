"""Tests for the bytes expectation helper."""
from __future__ import annotations

import pathlib

import pytest

from snappylapy.expectation_classes.expect_bytes import BytesExpect
from snappylapy.models import Settings
from snappylapy.session import SnapshotSession


@pytest.fixture
def bytes_expect(tmp_path: pathlib.Path) -> BytesExpect:
    """Provide a BytesExpect instance with temporary snapshot directories."""
    settings = Settings(
        test_filename="test_expect_bytes",
        test_function="test_case",
        snapshots_base_dir=tmp_path,
    )
    return BytesExpect(settings=settings, snappylapy_session=SnapshotSession())


def test_to_be_success(bytes_expect: BytesExpect) -> None:
    """The to_be assertion should pass on identical bytes."""
    payload = b"Hello, World!"
    bytes_expect(payload).to_be(b"Hello, World!")


def test_to_be_failure(bytes_expect: BytesExpect) -> None:
    """The to_be assertion should fail on different bytes."""
    payload = b"Hello, World!"
    with pytest.raises(AssertionError):
        bytes_expect(payload).to_be(b"Hello, Universe!")


def test_to_contain_success(bytes_expect: BytesExpect) -> None:
    """The to_contain assertion should pass when subsequence is present."""
    bytes_expect(b"Hello, World!").to_contain(b"World")
    bytes_expect(b"Hello, World!").to_contain(b"Hello")


def test_to_contain_failure(bytes_expect: BytesExpect) -> None:
    """The to_contain assertion should fail when subsequence is not present."""
    with pytest.raises(AssertionError, match="Expected bytes to contain"):
        bytes_expect(b"Hello, World!").to_contain(b"missing")


def test_to_not_contain_success(bytes_expect: BytesExpect) -> None:
    """The to_not_contain assertion should pass when subsequence is not present."""
    bytes_expect(b"Hello, World!").to_not_contain(b"missing")


def test_to_not_contain_failure(bytes_expect: BytesExpect) -> None:
    """The to_not_contain assertion should fail when subsequence is present."""
    with pytest.raises(AssertionError, match="Expected bytes to not contain"):
        bytes_expect(b"Hello, World!").to_not_contain(b"World")


def test_to_start_with_success(bytes_expect: BytesExpect) -> None:
    """The to_start_with assertion should pass when bytes starts with prefix."""
    bytes_expect(b"Hello, World!").to_start_with(b"Hello")


def test_to_start_with_failure(bytes_expect: BytesExpect) -> None:
    """The to_start_with assertion should fail when bytes doesn't start with prefix."""
    with pytest.raises(AssertionError, match="Expected bytes to start with"):
        bytes_expect(b"Hello, World!").to_start_with(b"World")


def test_to_end_with_success(bytes_expect: BytesExpect) -> None:
    """The to_end_with assertion should pass when bytes ends with suffix."""
    bytes_expect(b"Hello, World!").to_end_with(b"World!")


def test_to_end_with_failure(bytes_expect: BytesExpect) -> None:
    """The to_end_with assertion should fail when bytes doesn't end with suffix."""
    with pytest.raises(AssertionError, match="Expected bytes to end with"):
        bytes_expect(b"Hello, World!").to_end_with(b"Hello")


def test_to_have_length_success(bytes_expect: BytesExpect) -> None:
    """The to_have_length assertion should pass for correct length."""
    bytes_expect(b"Hello").to_have_length(5)


def test_to_have_length_failure(bytes_expect: BytesExpect) -> None:
    """The to_have_length assertion should fail for incorrect length."""
    with pytest.raises(AssertionError, match="Expected bytes length 10 but got 5"):
        bytes_expect(b"Hello").to_have_length(10)


def test_to_be_empty_success(bytes_expect: BytesExpect) -> None:
    """The to_be_empty assertion should pass for empty bytes."""
    bytes_expect(b"").to_be_empty()


def test_to_be_empty_failure(bytes_expect: BytesExpect) -> None:
    """The to_be_empty assertion should fail for non-empty bytes."""
    with pytest.raises(AssertionError, match="Expected bytes to be empty"):
        bytes_expect(b"not empty").to_be_empty()


def test_to_not_be_empty_success(bytes_expect: BytesExpect) -> None:
    """The to_not_be_empty assertion should pass for non-empty bytes."""
    bytes_expect(b"not empty").to_not_be_empty()


def test_to_not_be_empty_failure(bytes_expect: BytesExpect) -> None:
    """The to_not_be_empty assertion should fail for empty bytes."""
    with pytest.raises(AssertionError, match="Expected bytes to not be empty"):
        bytes_expect(b"").to_not_be_empty()


def test_to_decode_as_success(bytes_expect: BytesExpect) -> None:
    """The to_decode_as assertion should pass for correct decoding."""
    bytes_expect(b"Hello, World!").to_decode_as("Hello, World!")
    bytes_expect("Café".encode("utf-8")).to_decode_as("Café", "utf-8")


def test_to_decode_as_failure_content(bytes_expect: BytesExpect) -> None:
    """The to_decode_as assertion should fail for incorrect decoded content."""
    with pytest.raises(AssertionError, match="Expected bytes to decode to"):
        bytes_expect(b"Hello, World!").to_decode_as("Hello, Universe!")


def test_to_decode_as_failure_encoding(bytes_expect: BytesExpect) -> None:
    """The to_decode_as assertion should fail for invalid encoding."""
    with pytest.raises(AssertionError, match="Failed to decode bytes"):
        bytes_expect(b"\xff\xfe").to_decode_as("test", "ascii")


def test_to_match_regex_when_decoded_success(bytes_expect: BytesExpect) -> None:
    """The to_match_regex_when_decoded assertion should pass for matching patterns."""
    bytes_expect(b"test123").to_match_regex_when_decoded(r"\w+\d+")
    bytes_expect(b"email@domain.com").to_match_regex_when_decoded(r"\w+@\w+\.\w+")


def test_to_match_regex_when_decoded_failure(bytes_expect: BytesExpect) -> None:
    """The to_match_regex_when_decoded assertion should fail for non-matching patterns."""
    with pytest.raises(AssertionError, match="Expected decoded bytes to match regex pattern"):
        bytes_expect(b"test").to_match_regex_when_decoded(r"\d+")


def test_to_match_regex_when_decoded_encoding_error(bytes_expect: BytesExpect) -> None:
    """The to_match_regex_when_decoded assertion should fail for invalid encoding."""
    with pytest.raises(AssertionError, match="Failed to decode bytes"):
        bytes_expect(b"\xff\xfe").to_match_regex_when_decoded(r"\w+", "ascii")


def test_to_contain_any_of_success(bytes_expect: BytesExpect) -> None:
    """The to_contain_any_of assertion should pass when any subsequence is present."""
    bytes_expect(b"Hello, World!").to_contain_any_of([b"Hello", b"missing", b"also_missing"])


def test_to_contain_any_of_failure(bytes_expect: BytesExpect) -> None:
    """The to_contain_any_of assertion should fail when no subsequence is present."""
    with pytest.raises(AssertionError, match="Expected bytes to contain at least one of"):
        bytes_expect(b"Hello, World!").to_contain_any_of([b"missing", b"also_missing"])


def test_to_contain_all_of_success(bytes_expect: BytesExpect) -> None:
    """The to_contain_all_of assertion should pass when all subsequences are present."""
    bytes_expect(b"Hello, World!").to_contain_all_of([b"Hello", b"World"])


def test_to_contain_all_of_failure(bytes_expect: BytesExpect) -> None:
    """The to_contain_all_of assertion should fail when some subsequences are missing."""
    with pytest.raises(AssertionError, match="Expected bytes to contain all subsequences, missing:"):
        bytes_expect(b"Hello, World!").to_contain_all_of([b"Hello", b"missing"])


def test_to_be_truthy_success(bytes_expect: BytesExpect) -> None:
    """The to_be_truthy assertion should pass for non-empty bytes."""
    bytes_expect(b"non-empty").to_be_truthy()


def test_to_be_truthy_failure(bytes_expect: BytesExpect) -> None:
    """The to_be_truthy assertion should fail for empty bytes."""
    with pytest.raises(AssertionError, match="Expected bytes to be truthy"):
        bytes_expect(b"").to_be_truthy()


def test_to_be_falsy_success(bytes_expect: BytesExpect) -> None:
    """The to_be_falsy assertion should pass for empty bytes."""
    bytes_expect(b"").to_be_falsy()


def test_to_be_falsy_failure(bytes_expect: BytesExpect) -> None:
    """The to_be_falsy assertion should fail for non-empty bytes."""
    with pytest.raises(AssertionError, match="Expected bytes to be falsy"):
        bytes_expect(b"non-empty").to_be_falsy()


def test_ensure_data_available_no_data(bytes_expect: BytesExpect) -> None:
    """The _ensure_data_available method should raise when no data is prepared."""
    with pytest.raises(RuntimeError, match="No bytes data prepared yet"):
        bytes_expect.to_be_truthy()


def test_ensure_data_available_wrong_type(bytes_expect: BytesExpect) -> None:
    """The _ensure_data_available method should raise when data is not bytes."""
    bytes_expect._data = "not bytes"  # Force wrong type  # noqa: SLF001
    with pytest.raises(TypeError, match="Expected bytes data but received str"):
        bytes_expect.to_be_truthy()