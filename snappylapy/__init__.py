# ruff: noqa: I001, E402
"""Define the public api for the snappylapy package."""
import pytest
pytest.register_assert_rewrite("snappylapy.expectation_classes.base_snapshot")
from .fixtures import Expect, LoadSnapshot
from .marker import configure_snappylapy

__all__ = ["Expect", "LoadSnapshot", "configure_snappylapy"]
