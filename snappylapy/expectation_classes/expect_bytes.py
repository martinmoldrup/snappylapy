"""Snapshot testing and expectations for bytes."""

from __future__ import annotations

from .base_snapshot import BaseSnapshot
from snappylapy.serialization import BytesSerializer


class BytesExpect(BaseSnapshot[bytes]):
    """Snapshot testing for bytes."""

    serializer_class = BytesSerializer

    def __call__(self, data_to_snapshot: bytes, name: str | None = None, filetype: str = "bytes.txt") -> BytesExpect:
        """Prepare bytes for snapshot testing."""
        self._prepare_test(data_to_snapshot, name, filetype)
        return self
