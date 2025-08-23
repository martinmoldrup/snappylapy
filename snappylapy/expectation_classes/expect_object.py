"""Snapshot testing and expectations for generic custom objects."""
from __future__ import annotations

from .base_snapshot import BaseSnapshot
from snappylapy.serialization import JsonPickleSerializer


class ObjectExpect(BaseSnapshot[object]):
    """Snapshot testing for generic objects."""

    serializer_class = JsonPickleSerializer[object]

    def __call__(
        self,
        data_to_snapshot: object,
        name: str | None = None,
        filetype: str = "object.json",
    ) -> ObjectExpect:
        """Prepare an object for snapshot testing."""
        self._prepare_test(data_to_snapshot, name, filetype)
        return self
