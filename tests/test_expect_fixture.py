"""
Type resolution tests for `Expect.__call__` overloads.

These tests rely on `assert_type` so that static type checkers (mypy, pylance, pyright)
validate that each overload of `Expect.__call__` returns the correct *Expect class.
At runtime `assert_type` is a no-op returning the original value; we also add
`isinstance` assertions to guard dynamic dispatch.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import MagicMock

import pytest

try:  # Python <3.11 fallback
    from typing import assert_type  # type: ignore[attr-defined]
except ImportError:  # pragma: no cover
    from typing_extensions import assert_type  # type: ignore[attr-defined]

try:  # Optional dependency import for runtime test skipping logic
    import pandas as pd
except ImportError:  # pragma: no cover
    pd = None  # type: ignore[assignment]

from snappylapy.expectation_classes import (
    BytesExpect,
    DataframeExpect,
    DictExpect,
    ListExpect,
    StringExpect,
    ObjectExpect,
)
from snappylapy.fixtures import Expect
from snappylapy.models import Settings
from snappylapy.session import SnapshotSession


@pytest.fixture
def expect_fixture(tmp_path: Path) -> Expect:
    """Provide an `Expect` instance with minimal valid settings."""
    settings = Settings(
        test_filename="test_expect_type_overloads",
        test_function="test_func",
        snapshots_base_dir=tmp_path,
    )
    return Expect(SnapshotSession(), settings)


def test_overload_dict(expect_fixture: Expect) -> None:
    """Dict input returns DictExpect."""
    result = expect_fixture({"a": 1})
    assert isinstance(result, DictExpect)
    assert_type(result, DictExpect)


def test_overload_list(expect_fixture: Expect) -> None:
    """List input returns ListExpect."""
    result = expect_fixture([1, 2, 3])
    assert isinstance(result, ListExpect)
    assert_type(result, ListExpect)


def test_overload_string(expect_fixture: Expect) -> None:
    """String input returns StringExpect."""
    result = expect_fixture("hello")
    assert isinstance(result, StringExpect)
    assert_type(result, StringExpect)


def test_overload_bytes(expect_fixture: Expect) -> None:
    """Bytes input returns BytesExpect."""
    result = expect_fixture(b"data")
    assert isinstance(result, BytesExpect)
    assert_type(result, BytesExpect)


@pytest.mark.skipif(pd is None and not TYPE_CHECKING, reason="pandas not installed")
def test_overload_dataframe(expect_fixture: Expect) -> None:  # pragma: no cover - optional dependency
    """DataFrame input returns DataframeExpect (when pandas available)."""
    assert pd is not None  # for type checkers
    data_frame = pd.DataFrame({"a": [1, 2, 3]})
    result = expect_fixture(data_frame)
    assert isinstance(result, DataframeExpect)
    assert_type(result, DataframeExpect)

def test_overload_object(expect_fixture: Expect) -> None:
    """Object input returns ObjectExpect."""
    class Custom:
        pass

    result = expect_fixture(Custom())
    assert isinstance(result, ObjectExpect)
    assert_type(result, ObjectExpect)

@pytest.mark.parametrize(
    "data,expected_attr",
    [
        ({"a": 1}, "dict"),
        ([1, 2, 3], "list"),
        ("hello", "string"),
        (b"bytes", "bytes"),
    ],
)
def test_expect_selects_correct_class_for_builtin_types(data, expected_attr, expect_fixture):
    """Test that Expect.__call__ selects the correct class for builtin types."""
    # Patch all expectation attributes with mocks
    expect_fixture.dict = MagicMock(return_value="called_dict")
    expect_fixture.list = MagicMock(return_value="called_list")
    expect_fixture.string = MagicMock(return_value="called_string")
    expect_fixture.bytes = MagicMock(return_value="called_bytes")
    expect_fixture.dataframe = MagicMock(return_value="called_dataframe")
    expect_fixture.object = MagicMock(return_value="called_object")
    result = expect_fixture(data)
    assert result == f"called_{expected_attr}"
    getattr(expect_fixture, expected_attr).assert_called_once_with(data)


def test_expect_selects_object_for_custom_type(expect_fixture: Expect):
    """Test that Expect.__call__ falls back to object for custom types."""
    class Custom:
        pass

    custom_obj = Custom()
    expect_fixture.dict = MagicMock(return_value="called_dict")
    expect_fixture.list = MagicMock(return_value="called_list")
    expect_fixture.string = MagicMock(return_value="called_string")
    expect_fixture.bytes = MagicMock(return_value="called_bytes")
    expect_fixture.dataframe = MagicMock(return_value="called_dataframe")
    expect_fixture.object = MagicMock(return_value="called_object")
    result = expect_fixture(custom_obj)
    assert result == "called_object"
    expect_fixture.object.assert_called_once_with(custom_obj)
