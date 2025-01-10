"""Snapshot testing and expectations for lists."""
from __future__ import annotations

from .base_snapshot import BaseSnapshot
from snappylapy.serialization import JsonPickleSerializer
from typing import Any


class ListExpect(BaseSnapshot[list[Any]]):
    """Snapshot testing for lists."""

    serializer_class = JsonPickleSerializer[list[Any]]

    def __call__(
        self,
        data_to_snapshot: list[Any],
        name: str = "",
        filetype: str = "list.json",
    ) -> ListExpect:
        """Prepare a list for snapshot testing."""
        self._prepare_test(data_to_snapshot, name, filetype)
        return self
