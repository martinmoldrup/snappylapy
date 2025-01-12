"""
The fixtures module provides classes returned by fixtures registred by pytest in snappylapy.

Snappylapy provides the following fixtures.

- expect: Expect
    - Allows for validating various expectations on the test results and do snapshot testing.
- load_snapshot: LoadSnapshot
    - Allows loading from a snapshot created by another test.
"""
from __future__ import annotations

import pathlib
from .expectation_classes import (
    BytesExpect,
    DictExpect,
    ListExpect,
    StringExpect,
)
from .models import Settings
from .serialization import (
    BytesSerializer,
    JsonPickleSerializer,
    StringSerializer,
)
from typing import Any


class Expect:
    """Snapshot testing class."""

    def __init__(
            self,
            update_snapshots: bool,  # noqa: FBT001
    ) -> None:
        """Initialize the snapshot testing."""
        self.settings = Settings()
        self.dict = DictExpect(update_snapshots, self.settings)
        self.list = ListExpect(update_snapshots, self.settings)
        self.string = StringExpect(update_snapshots, self.settings)
        self.bytes = BytesExpect(update_snapshots, self.settings)

    def read_snapshot(self) -> bytes:
        """Read the snapshot file."""
        return (self.settings.snapshot_dir /
                self.settings.filename).read_bytes()

    def read_test_results(self) -> bytes:
        """Read the test results file."""
        return (self.settings.test_results_dir /
                self.settings.filename).read_bytes()

    @property
    def snapshot_dir(self) -> pathlib.Path:
        """Get the snapshot directory."""
        return self.settings.snapshot_dir

    @snapshot_dir.setter
    def snapshot_dir(self, value: str | pathlib.Path) -> None:
        """Set the snapshot directory."""
        self.settings.snapshot_dir = pathlib.Path(value) if isinstance(
            value, str) else value

    @property
    def test_results_dir(self) -> pathlib.Path:
        """Get the test results directory."""
        return self.settings.test_results_dir

    @test_results_dir.setter
    def test_results_dir(self, value: str | pathlib.Path) -> None:
        """Set the test results directory."""
        self.settings.test_results_dir = pathlib.Path(value) if isinstance(
            value, str) else value


class LoadSnapshot:
    """Snapshot loading class."""

    def __init__(self, settings: Settings) -> None:
        """Initialize the snapshot loading."""
        self.settings = settings

    @property
    def snapshot_dir(self) -> pathlib.Path:
        """Get the snapshot directory."""
        return self.settings.snapshot_dir

    @snapshot_dir.setter
    def snapshot_dir(self, value: str | pathlib.Path) -> None:
        """Set the snapshot directory."""
        self.settings.snapshot_dir = pathlib.Path(value) if isinstance(
            value, str) else value

    def _read_snapshot(self) -> bytes:
        """Read the snapshot file."""
        return (self.settings.snapshot_dir /
                self.settings.filename).read_bytes()

    def dict(self) -> dict:
        """Load dictionary snapshot."""
        self.settings.filename_extension = "dict.json"
        return JsonPickleSerializer[dict]().deserialize(self._read_snapshot())

    def list(self) -> list[Any]:
        """Load list snapshot."""
        self.settings.filename_extension = "list.json"
        return JsonPickleSerializer[list[Any]]().deserialize(
            self._read_snapshot())

    def string(self) -> str:
        """Load string snapshot."""
        self.settings.filename_extension = "string.txt"
        return StringSerializer().deserialize(self._read_snapshot())

    def bytes(self) -> bytes:
        """Load bytes snapshot."""
        self.settings.filename_extension = "bytes.txt"
        return BytesSerializer().deserialize(self._read_snapshot())
