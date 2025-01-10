"""Snapshot testing and expectations for dicts."""
from __future__ import annotations

from .base_snapshot import BaseSnapshot
from snappylapy.serialization import JsonPickleSerializer


class DictExpect(BaseSnapshot[dict]):
    """Snapshot testing for dictionaries."""

    serializer_class = JsonPickleSerializer[dict]

    def __call__(self,
                 data_to_snapshot: dict,
                 name: str = "",
                 filetype: str = "dict.json") -> DictExpect:
        """Prepare a dictionary for snapshot testing."""
        self._prepare_test(data_to_snapshot, name, filetype)
        return self
