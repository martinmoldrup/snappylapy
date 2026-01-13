"""Snapshot testing and expectations for strings."""

from __future__ import annotations

from .base_snapshot import BaseSnapshot
from snappylapy.serialization import StringSerializer


class StringExpect(BaseSnapshot[str]):
    """Snapshot testing for strings."""

    serializer_class = StringSerializer

    def __call__(self, data_to_snapshot: str, name: str | None = None, filetype: str = "string.txt") -> StringExpect:
        """Prepare a string for snapshot testing."""
        if not hasattr(data_to_snapshot, "encode"):
            msg = f"data_to_snapshot of type {type(data_to_snapshot)} must be a string-like object supporting an 'encode' method."  # noqa: E501
            raise TypeError(msg)
        self._prepare_test(data_to_snapshot, name, filetype)
        return self
