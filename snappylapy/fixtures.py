"""
The fixtures module provides classes returned by fixtures registered by pytest in snappylapy.

Snappylapy provides the following fixtures.

- expect: Expect
    - Allows for validating various expectations on the test results and do snapshot testing.
- load_snapshot: LoadSnapshot
    - Allows loading from a snapshot created by another test.
"""

from __future__ import annotations

from .expectation_classes import (
    BytesExpect,
    DataframeExpect,
    DictExpect,
    ListExpect,
    ObjectExpect,
    StringExpect,
)
from .models import Settings
from .serialization import (
    BytesSerializer,
    JsonPickleSerializer,
    StringSerializer,
)
from snappylapy.constants import DIRECTORY_NAMES
from snappylapy.session import SnapshotSession
from typing import Any, Protocol, overload


class _CallableExpectation(Protocol):
    """Protocol for callable expectations to use internally in this module."""

    def __call__(
        self,
        data_to_snapshot: Any,  # noqa: ANN401
        name: str | None = None,
        filetype: str = "snapshot.txt",
    ) -> DictExpect | ListExpect | StringExpect | BytesExpect | DataframeExpect:
        """Call the expectation with the given parameters."""
        ...


class Expect:
    """
    Snapshot testing fixture class.

    Do not instantiate this class directly, instead use the `expect` fixture provided by pytest.
    Use this class as a type hint for the `expect` fixture.

    Example:
    -------
    ```python
    from snappylapy.fixtures import Expect


    def test_example(expect: Expect) -> None:
        expect.dict({"key": "value"}).to_match_snapshot()
    ```

    """

    def __init__(
        self,
        snappylapy_session: SnapshotSession,
        snappylapy_settings: Settings,
    ) -> None:
        """Initialize the snapshot testing."""
        self.settings = snappylapy_settings

        self.dict = DictExpect(self.settings, snappylapy_session)
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

        self.list = ListExpect(self.settings, snappylapy_session)
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

        self.string = StringExpect(self.settings, snappylapy_session)
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

        self.bytes = BytesExpect(self.settings, snappylapy_session)
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

        self.dataframe = DataframeExpect(self.settings, snappylapy_session)
        """DataframeExpect instance for configuring snapshot testing of dataframes.

        The instance is callable with the following parameters:

        Parameters
        ----------
        data_to_snapshot : pd.DataFrame
            The dataframe data to be snapshotted.
        name : str, optional
            The name of the snapshot, by default "".
        filetype : str, optional
            The file type of the snapshot, by default "dataframe.json".

        Returns
        -------
        DataframeExpect
            The instance of the DataframeExpect class.
            This class can be used for doing actual expectations on the dataframe.

        Example
        -------
        ```python
        import pandas as pd
        from snappylapy.fixtures import Expect
        def test_dataframe(expect: Expect) -> None:
            df = pd.DataFrame({"key": ["value1", "value2"]})
            expect.dataframe(df).to_match_snapshot()
        ```
        """

        self.object = ObjectExpect(self.settings, snappylapy_session)
        """ObjectExpect instance for configuring snapshot testing of generic objects.

        The instance is callable with the following parameters:

        Parameters
        ----------
        data_to_snapshot : object
            The object data to be snapshotted.
        name : str, optional
            The name of the snapshot, by default "".
        filetype : str, optional
            The file type of the snapshot, by default "object.json".

        Returns
        -------
        ObjectExpect
            The instance of the ObjectExpect class.

        Example
        -------
        ```python
        expect.object({"key": "value"}).to_match_snapshot()
        ```
        """

    def read_snapshot(self) -> bytes:
        """Read the snapshot file."""
        return (self.settings.snapshot_dir / self.settings.filename).read_bytes()

    def read_test_results(self) -> bytes:
        """Read the test results file."""
        return (self.settings.test_results_dir / self.settings.filename).read_bytes()

    @overload
    def __call__(self, data_to_snapshot: dict, name: str | None = None, filetype: str | None = None) -> DictExpect: ...

    @overload
    def __call__(
        self,
        data_to_snapshot: list[Any],
        name: str | None = None,
        filetype: str | None = None,
    ) -> ListExpect: ...

    @overload
    def __call__(self, data_to_snapshot: str, name: str | None = None, filetype: str | None = None) -> StringExpect: ...

    @overload
    def __call__(
        self,
        data_to_snapshot: bytes,
        name: str | None = None,
        filetype: str | None = None,
    ) -> BytesExpect: ...

    @overload
    def __call__(
        self,
        data_to_snapshot: DataframeExpect.DataFrame,
        name: str | None = None,
        filetype: str | None = None,
    ) -> DataframeExpect: ...

    @overload
    def __call__(
        self,
        data_to_snapshot: Any,  # noqa: ANN401
        name: str | None = None,
        filetype: str | None = None,
    ) -> ObjectExpect: ...

    def __call__(
        self,
        data_to_snapshot: dict | list[Any] | str | bytes | DataframeExpect.DataFrame,
        name: str | None = None,
        filetype: str | None = None,
    ) -> DictExpect | ListExpect | StringExpect | BytesExpect | DataframeExpect | ObjectExpect:
        """Call the fixture with the given parameters. Falls back to object handler for custom objects."""
        kwargs: dict[str, str] = {}
        if name is not None:
            kwargs["name"] = name
        if filetype is not None:
            kwargs["filetype"] = filetype

        type_map: dict[type, _CallableExpectation] = {
            dict: self.dict,
            list: self.list,
            str: self.string,
            bytes: self.bytes,
            DataframeExpect.DataFrame: self.dataframe,
        }

        for typ, func in type_map.items():
            if isinstance(typ, type) and isinstance(data_to_snapshot, typ):
                return func(data_to_snapshot, **kwargs)

        # Check if the object is a pandas DataFrame without importing pandas directly
        if (
            type(data_to_snapshot).__module__.startswith("pandas")
            and type(data_to_snapshot).__name__ == "DataFrame"
            # TODO: Create a protocol class instead that contains all the dependencies we are depending on
        ):
            return self.dataframe(data_to_snapshot, **kwargs)  # type: ignore[arg-type]

        # Fallback: treat custom objects as dicts for snapshotting
        return self.object(data_to_snapshot, **kwargs)


class LoadSnapshot:
    """Snapshot loading class."""

    def __init__(self, settings: Settings) -> None:
        """Initialize the snapshot loading."""
        self.settings = settings

    def _read_snapshot(self) -> bytes:
        """Read the snapshot file."""
        if not self.settings.depending_snapshots_base_dir:
            msg = "Depending snapshots base directory is not set."
            raise ValueError(msg)
        return (
            self.settings.depending_snapshots_base_dir
            / DIRECTORY_NAMES.snapshot_dir_name
            / self.settings.depending_filename
        ).read_bytes()

    def dict(self) -> dict:
        """Load dictionary snapshot."""
        self.settings.depending_filename_extension = "dict.json"
        return JsonPickleSerializer[dict]().deserialize(self._read_snapshot())

    def list(self) -> list[Any]:
        """Load list snapshot."""
        self.settings.depending_filename_extension = "list.json"
        return JsonPickleSerializer[list[Any]]().deserialize(self._read_snapshot())

    def string(self) -> str:
        """Load string snapshot."""
        self.settings.depending_filename_extension = "string.txt"
        return StringSerializer().deserialize(self._read_snapshot())

    def bytes(self) -> bytes:
        """Load bytes snapshot."""
        self.settings.depending_filename_extension = "bytes.txt"
        return BytesSerializer().deserialize(self._read_snapshot())

    def dataframe(self) -> DataframeExpect.DataFrame:
        """Load dataframe snapshot."""
        self.settings.depending_filename_extension = "dataframe.json"
        return DataframeExpect.DataFrame(
            JsonPickleSerializer[DataframeExpect.DataFrame]().deserialize(self._read_snapshot()),
        )
