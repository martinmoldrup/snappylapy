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
from snappylapy.session import SnapshotSession


class Expect:
    """
    Snapshot testing fixture class.
    Do not instantiate this class directly, insatead use the `expect` fixture provided by pytest.
    Use this class as a type hint for the `expect` fixture.

    Example
    -------
    ```python
    from snappylapy.fixtures import Expect

    def test_example(expect: Expect) -> None:
        expect.dict({"key": "value"}).to_match_snapshot()
    ```
    """

    def __init__(
        self,
        update_snapshots: bool,  # noqa: FBT001
        test_filename: str,
        test_function: str,
        snappylapy_session: SnapshotSession,
    ) -> None:
        """Initialize the snapshot testing."""
        self.settings = Settings(
            test_filename=test_filename,
            test_function=test_function,
            snapshot_update=update_snapshots,
        )
        self.dict = DictExpect(update_snapshots, self.settings, snappylapy_session)
        """DictExpect instance for configuring snapshot testing of dictionaries. 
        The instance is callable with the following parameters:

        Parameters
        ----------
        data_to_snapshot : dict
            The dictionary data to be snapshotted.
        name : str, optional
            The name of the snapshot, by default "".
        filetype : str, optional
            The file type of the snapshot, by default "dict.json".

        Returns
        -------
        DictExpect
            The instance of the DictExpect class.

        Example
        -------
        ```python
        expect.dict({"key": "value"}).to_match_snapshot()
        expect.dict({"key": "value"}, name="snapshot_name", filetype="json").to_match_snapshot()
        ```
        """

        self.list = ListExpect(update_snapshots, self.settings, snappylapy_session)
        """ListExpect instance for configuring snapshot testing of lists. 
        The instance is callable with the following parameters:

        Parameters
        ----------
        data_to_snapshot : list
            The list data to be snapshotted.
        name : str, optional
            The name of the snapshot, by default "".
        filetype : str, optional
            The file type of the snapshot, by default "list.json".

        Returns
        -------
        ListExpect
            The instance of the ListExpect class.

        Example
        -------
        ```python
        expect.list([1, 2, 3]).to_match_snapshot()
        ```
        """

        self.string = StringExpect(update_snapshots, self.settings, snappylapy_session)
        """StringExpect instance for configuring snapshot testing of strings. 
        The instance is callable with the following parameters:

        Parameters
        ----------
        data_to_snapshot : str
            The string data to be snapshotted.
        name : str, optional
            The name of the snapshot, by default "".
        filetype : str, optional
            The file type of the snapshot, by default "string.txt".

        Returns
        -------
        StringExpect
            The instance of the StringExpect class.

        Example
        -------
        ```python
        expect.string("Hello, World!").to_match_snapshot()
        ```
        """

        self.bytes = BytesExpect(update_snapshots, self.settings, snappylapy_session)
        """BytesExpect instance for configuring snapshot testing of bytes. 
        The instance is callable with the following parameters:

        Parameters
        ----------
        data_to_snapshot : bytes
            The bytes data to be snapshotted.
        name : str, optional
            The name of the snapshot, by default "".
        filetype : str, optional
            The file type of the snapshot, by default "bytes.txt".

        Returns
        -------
        BytesExpect
            The instance of the BytesExpect class.

        Example
        -------
        ```python
        expect.bytes(b"binary data").to_match_snapshot()
        ```
        """

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
