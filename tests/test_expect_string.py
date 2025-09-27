"""Testing of the string test expectations class."""
from __future__ import annotations

import pathlib
from unittest import mock

import pytest

import snappylapy.expectation_classes.expect_string as module_on_test
from snappylapy.models import Settings


@pytest.fixture
def expect() -> module_on_test.StringExpect:
    """Provide a StringExpect instance with mocked session."""
    snappylapy_session = mock.MagicMock()
    return module_on_test.StringExpect(
        settings=Settings(
            test_filename="test_file.py",
            test_function="test_function",
            custom_name=None,
            snapshots_base_dir=pathlib.Path("/snapshots"),
            snapshot_update=False,
            filename_extension="txt",
            depending_test_filename=None,
            depending_test_function=None,
            depending_filename_extension=None,
            depending_snapshots_base_dir=None,
        ),
        snappylapy_session=snappylapy_session,
    )


def test_string_fuzzy_match(expect: module_on_test.StringExpect) -> None:
    """Test fuzzy matching functionality."""
    string_gotten = "Hello, World!"
    string_expected = "Hello, World!"
    expect(string_gotten).to_fuzzy_match(string_expected)


def test_to_be_success(expect: module_on_test.StringExpect) -> None:
    """The to_be assertion should pass on identical strings."""
    expect("test string").to_be("test string")


def test_to_be_failure(expect: module_on_test.StringExpect) -> None:
    """The to_be assertion should fail on different strings."""
    with pytest.raises(AssertionError):
        expect("test string").to_be("different string")


def test_to_contain_success(expect: module_on_test.StringExpect) -> None:
    """The to_contain assertion should pass when substring is present."""
    expect("Hello, World!").to_contain("World")
    expect("Hello, World!").to_contain("Hello")


def test_to_contain_failure(expect: module_on_test.StringExpect) -> None:
    """The to_contain assertion should fail when substring is not present."""
    with pytest.raises(AssertionError, match="Expected string to contain 'missing'"):
        expect("Hello, World!").to_contain("missing")


def test_to_not_contain_success(expect: module_on_test.StringExpect) -> None:
    """The to_not_contain assertion should pass when substring is not present."""
    expect("Hello, World!").to_not_contain("missing")


def test_to_not_contain_failure(expect: module_on_test.StringExpect) -> None:
    """The to_not_contain assertion should fail when substring is present."""
    with pytest.raises(AssertionError, match="Expected string to not contain 'World'"):
        expect("Hello, World!").to_not_contain("World")


def test_to_start_with_success(expect: module_on_test.StringExpect) -> None:
    """The to_start_with assertion should pass when string starts with prefix."""
    expect("Hello, World!").to_start_with("Hello")


def test_to_start_with_failure(expect: module_on_test.StringExpect) -> None:
    """The to_start_with assertion should fail when string doesn't start with prefix."""
    with pytest.raises(AssertionError, match="Expected string to start with 'World'"):
        expect("Hello, World!").to_start_with("World")


def test_to_end_with_success(expect: module_on_test.StringExpect) -> None:
    """The to_end_with assertion should pass when string ends with suffix."""
    expect("Hello, World!").to_end_with("World!")


def test_to_end_with_failure(expect: module_on_test.StringExpect) -> None:
    """The to_end_with assertion should fail when string doesn't end with suffix."""
    with pytest.raises(AssertionError, match="Expected string to end with 'Hello'"):
        expect("Hello, World!").to_end_with("Hello")


def test_to_have_length_success(expect: module_on_test.StringExpect) -> None:
    """The to_have_length assertion should pass for correct length."""
    expect("Hello").to_have_length(5)


def test_to_have_length_failure(expect: module_on_test.StringExpect) -> None:
    """The to_have_length assertion should fail for incorrect length."""
    with pytest.raises(AssertionError, match="Expected string length 10 but got 5"):
        expect("Hello").to_have_length(10)


def test_to_be_empty_success(expect: module_on_test.StringExpect) -> None:
    """The to_be_empty assertion should pass for empty strings."""
    expect("").to_be_empty()


def test_to_be_empty_failure(expect: module_on_test.StringExpect) -> None:
    """The to_be_empty assertion should fail for non-empty strings."""
    with pytest.raises(AssertionError, match="Expected string to be empty"):
        expect("not empty").to_be_empty()


def test_to_not_be_empty_success(expect: module_on_test.StringExpect) -> None:
    """The to_not_be_empty assertion should pass for non-empty strings."""
    expect("not empty").to_not_be_empty()


def test_to_not_be_empty_failure(expect: module_on_test.StringExpect) -> None:
    """The to_not_be_empty assertion should fail for empty strings."""
    with pytest.raises(AssertionError, match="Expected string to not be empty"):
        expect("").to_not_be_empty()


def test_to_match_regex_success(expect: module_on_test.StringExpect) -> None:
    """The to_match_regex assertion should pass for matching patterns."""
    expect("test123").to_match_regex(r"\w+\d+")
    expect("email@domain.com").to_match_regex(r"\w+@\w+\.\w+")


def test_to_match_regex_failure(expect: module_on_test.StringExpect) -> None:
    """The to_match_regex assertion should fail for non-matching patterns."""
    with pytest.raises(AssertionError, match="Expected string to match regex pattern"):
        expect("test").to_match_regex(r"\d+")


def test_to_not_match_regex_success(expect: module_on_test.StringExpect) -> None:
    """The to_not_match_regex assertion should pass for non-matching patterns."""
    expect("test").to_not_match_regex(r"\d+")


def test_to_not_match_regex_failure(expect: module_on_test.StringExpect) -> None:
    """The to_not_match_regex assertion should fail for matching patterns."""
    with pytest.raises(AssertionError, match="Expected string to not match regex pattern"):
        expect("test123").to_not_match_regex(r"\w+\d+")


def test_to_be_uppercase_success(expect: module_on_test.StringExpect) -> None:
    """The to_be_uppercase assertion should pass for uppercase strings."""
    expect("HELLO").to_be_uppercase()


def test_to_be_uppercase_failure(expect: module_on_test.StringExpect) -> None:
    """The to_be_uppercase assertion should fail for non-uppercase strings."""
    with pytest.raises(AssertionError, match="Expected string to be uppercase"):
        expect("hello").to_be_uppercase()


def test_to_be_lowercase_success(expect: module_on_test.StringExpect) -> None:
    """The to_be_lowercase assertion should pass for lowercase strings."""
    expect("hello").to_be_lowercase()


def test_to_be_lowercase_failure(expect: module_on_test.StringExpect) -> None:
    """The to_be_lowercase assertion should fail for non-lowercase strings."""
    with pytest.raises(AssertionError, match="Expected string to be lowercase"):
        expect("HELLO").to_be_lowercase()


def test_to_be_title_case_success(expect: module_on_test.StringExpect) -> None:
    """The to_be_title_case assertion should pass for title case strings."""
    expect("Hello World").to_be_title_case()


def test_to_be_title_case_failure(expect: module_on_test.StringExpect) -> None:
    """The to_be_title_case assertion should fail for non-title case strings."""
    with pytest.raises(AssertionError, match="Expected string to be in title case"):
        expect("hello world").to_be_title_case()


def test_to_be_numeric_success(expect: module_on_test.StringExpect) -> None:
    """The to_be_numeric assertion should pass for numeric strings."""
    expect("12345").to_be_numeric()


def test_to_be_numeric_failure(expect: module_on_test.StringExpect) -> None:
    """The to_be_numeric assertion should fail for non-numeric strings."""
    with pytest.raises(AssertionError, match="Expected string to be numeric"):
        expect("123abc").to_be_numeric()


def test_to_be_alphabetic_success(expect: module_on_test.StringExpect) -> None:
    """The to_be_alphabetic assertion should pass for alphabetic strings."""
    expect("hello").to_be_alphabetic()


def test_to_be_alphabetic_failure(expect: module_on_test.StringExpect) -> None:
    """The to_be_alphabetic assertion should fail for non-alphabetic strings."""
    with pytest.raises(AssertionError, match="Expected string to be alphabetic"):
        expect("hello123").to_be_alphabetic()


def test_to_be_alphanumeric_success(expect: module_on_test.StringExpect) -> None:
    """The to_be_alphanumeric assertion should pass for alphanumeric strings."""
    expect("hello123").to_be_alphanumeric()


def test_to_be_alphanumeric_failure(expect: module_on_test.StringExpect) -> None:
    """The to_be_alphanumeric assertion should fail for non-alphanumeric strings."""
    with pytest.raises(AssertionError, match="Expected string to be alphanumeric"):
        expect("hello-123").to_be_alphanumeric()


def test_to_contain_any_of_success(expect: module_on_test.StringExpect) -> None:
    """The to_contain_any_of assertion should pass when any substring is present."""
    expect("Hello, World!").to_contain_any_of(["Hello", "missing", "also_missing"])


def test_to_contain_any_of_failure(expect: module_on_test.StringExpect) -> None:
    """The to_contain_any_of assertion should fail when no substring is present."""
    with pytest.raises(AssertionError, match="Expected string to contain at least one of"):
        expect("Hello, World!").to_contain_any_of(["missing", "also_missing"])


def test_to_contain_all_of_success(expect: module_on_test.StringExpect) -> None:
    """The to_contain_all_of assertion should pass when all substrings are present."""
    expect("Hello, World!").to_contain_all_of(["Hello", "World"])


def test_to_contain_all_of_failure(expect: module_on_test.StringExpect) -> None:
    """The to_contain_all_of assertion should fail when some substrings are missing."""
    with pytest.raises(AssertionError, match="Expected string to contain all substrings, missing:"):
        expect("Hello, World!").to_contain_all_of(["Hello", "missing"])


def test_to_fuzzy_match_success(expect: module_on_test.StringExpect) -> None:
    """The to_fuzzy_match assertion should pass for similar strings."""
    expect("Hello, World!").to_fuzzy_match("Hello, World!", 1.0)
    expect("Hello, World!").to_fuzzy_match("Hello, Wrld!", 0.8)


def test_to_fuzzy_match_failure(expect: module_on_test.StringExpect) -> None:
    """The to_fuzzy_match assertion should fail for dissimilar strings."""
    with pytest.raises(AssertionError, match="Expected similarity"):
        expect("Hello, World!").to_fuzzy_match("Completely different", 0.8)


def test_to_be_truthy_success(expect: module_on_test.StringExpect) -> None:
    """The to_be_truthy assertion should pass for non-empty strings."""
    expect("non-empty").to_be_truthy()


def test_to_be_truthy_failure(expect: module_on_test.StringExpect) -> None:
    """The to_be_truthy assertion should fail for empty strings."""
    with pytest.raises(AssertionError, match="Expected string to be truthy"):
        expect("").to_be_truthy()


def test_to_be_falsy_success(expect: module_on_test.StringExpect) -> None:
    """The to_be_falsy assertion should pass for empty strings."""
    expect("").to_be_falsy()


def test_to_be_falsy_failure(expect: module_on_test.StringExpect) -> None:
    """The to_be_falsy assertion should fail for non-empty strings."""
    with pytest.raises(AssertionError, match="Expected string to be falsy"):
        expect("non-empty").to_be_falsy()


def test_ensure_data_available_no_data(expect: module_on_test.StringExpect) -> None:
    """The _ensure_data_available method should raise when no data is prepared."""
    with pytest.raises(RuntimeError, match="No string data prepared yet"):
        expect.to_be_truthy()


def test_ensure_data_available_wrong_type(expect: module_on_test.StringExpect) -> None:
    """The _ensure_data_available method should raise when data is not a string."""
    expect._data = 123  # Force wrong type  # noqa: SLF001
    with pytest.raises(TypeError, match="Expected string data but received int"):
        expect.to_be_truthy()
