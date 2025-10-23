"""
The fixtures module provides classes returned by fixtures registered by pytest in snappylapy.

Snappylapy provides the following pytest fixtures.

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
    PandasCsvSerializer,
    Serializer,
    StringSerializer,
)
from snappylapy.constants import DIRECTORY_NAMES
from snappylapy.session import SnapshotSession
from typing import Any, Protocol, TypeVar, overload

T = TypeVar("T")


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

    *Calling expect directly*

    The `expect` fixture can be called directly with a value, and it will automatically select
    the appropriate handler (DictExpect, ListExpect, StringExpect, BytesExpect, DataframeExpect, or ObjectExpect)
    depending on the type of the input. The input type must be resolvable to one of the supported types.

    Example usage
    ---------------
    `test_expect_direct_call.py`
    ```python
    from snappylapy.fixtures import Expect

    def test_expect_direct_call(expect: Expect) -> None:
        # Dict input
        data_dict: dict[str, int] = {"a": 1, "b": 2}
        expect(data_dict).to_match_snapshot()

        # List input
        data_list: list[int] = [1, 2, 3]
        expect(data_list).to_match_snapshot()

        # String input
        data_str: str = "pytest example"
        expect(data_str).to_match_snapshot()

        # Bytes input
        data_bytes: bytes = b"binary"
        expect(data_bytes).to_match_snapshot()

        # DataFrame input (requires pandas)
        import pandas as pd
        df: pd.DataFrame = pd.DataFrame({"x": [1, 2]})
        expect(df).to_match_snapshot()

        # Custom object input (falls back to ObjectExpect)
        class Custom:
            def __init__(self) -> None:
                self.value = 42
        custom_obj = Custom()
        expect(custom_obj).to_match_snapshot()
    ```

    The handler is chosen based on the type of `data_to_snapshot`. If the type is not directly supported,
    it falls back to the generic object handler.
    """

    def __init__(
        self,
        snappylapy_session: SnapshotSession,
        snappylapy_settings: Settings,
    ) -> None:
        """"""  # noqa: D419, blank, since used in doc generation
        self.settings = snappylapy_settings

        self.dict = DictExpect(self.settings, snappylapy_session)
        """DictExpect instance for configuring snapshot testing of dictionaries.

        The instance is callable with the following parameters:

        Parameters
        ----------
        - `data_to_snapshot` (`dict`): The dictionary data to be snapshotted.
        - `name` (`str`, optional): The name of the snapshot".
        - `filetype` (`str`, optional): The file type of the snapshot, by default "dict.json".

        Returns
        -------
        DictExpect
        - `DictExpect`: The instance of the DictExpect class.

        Example
        -------
        `test_fixture_expect_dict.py`
        ```python
        import pytest
        from snappylapy.fixtures import Expect

        def test_expect_dict(expect: Expect) -> None:
            data: dict[str, str] = {"key": "value"}
            expect.dict(data).to_match_snapshot()
            expect.dict(data, name="snapshot_name", filetype="dict.json").to_match_snapshot()
        ```
        """

        self.list = ListExpect(self.settings, snappylapy_session)
        """ListExpect instance for configuring snapshot testing of lists.

        The instance is callable with the following parameters:

        Parameters
        ----------
        - `data_to_snapshot` (`list`): The list data to be snapshotted.
        - `name` (`str`, optional): The name of the snapshot.
        - `filetype` (`str`, optional): The file type of the snapshot, by default "list.json".

        Returns
        -------
        ListExpect
        - `ListExpect`: The instance of the ListExpect class.

        Example
        -------
        `test_fixture_expect_list.py`
        ```python
        import pytest
        from snappylapy.fixtures import Expect

        def test_expect_list(expect: Expect) -> None:
            data: list[int] = [1, 2, 3]
            expect.list(data).to_match_snapshot()
        ```
        """

        self.string = StringExpect(self.settings, snappylapy_session)
        """StringExpect instance for configuring snapshot testing of strings.

        The instance is callable with the following parameters:

        Parameters
        ----------
        - `data_to_snapshot` (`str`): The string data to be snapshotted.
        - `name` (`str`, optional): The name of the snapshot.
        - `filetype` (`str`, optional): The file type of the snapshot, by default "string.txt".

        Returns
        -------
        StringExpect
        - `StringExpect`: The instance of the StringExpect class.

        Example
        -------
        `test_fixture_expect_string.py`
        ```python
        import pytest
        from snappylapy.fixtures import Expect

        def test_expect_string(expect: Expect) -> None:
            data: str = "Hello, World!"
            expect.string(data).to_match_snapshot()
        ```
        """

        self.bytes = BytesExpect(self.settings, snappylapy_session)
        """BytesExpect instance for configuring snapshot testing of bytes.

        The instance is callable with the following parameters:

        Parameters
        ----------
        - `data_to_snapshot` (`bytes`): The bytes data to be snapshotted.
        - `name` (`str`, optional): The name of the snapshot.
        - `filetype` (`str`, optional): The file type of the snapshot, by default "bytes.txt".

        Returns
        -------
        BytesExpect
        - `BytesExpect`: The instance of the BytesExpect class.

        Example
        -------
        `test_fixture_expect_bytes.py`
        ```python
        import pytest
        from snappylapy.fixtures import Expect

        def test_expect_bytes(expect: Expect) -> None:
            data: bytes = b"binary data"
            expect.bytes(data).to_match_snapshot()
        ```
        """

        self.dataframe = DataframeExpect(self.settings, snappylapy_session)
        """DataframeExpect instance for configuring snapshot testing of dataframes.

        The instance is callable with the following parameters:

        Parameters
        ----------
        - `data_to_snapshot` (`pd.DataFrame`): The dataframe data to be snapshotted.
        - `name` (`str`, optional): The name of the snapshot.
        - `filetype` (`str`, optional): The file type of the snapshot, by default "dataframe.json".

        Returns
        -------
        DataframeExpect
        - `DataframeExpect`: The instance of the DataframeExpect class.

        Example
        -------
        `test_fixture_expect_dataframe.py`
        ```python
        import pytest
        import pandas as pd
        from snappylapy.fixtures import Expect

        def test_expect_dataframe(expect: Expect) -> None:
            df: pd.DataFrame = pd.DataFrame({"key": ["value1", "value2"]})
            expect.dataframe(df).to_match_snapshot()
        ```
        """

        self.object = ObjectExpect(self.settings, snappylapy_session)
        """ObjectExpect instance for configuring snapshot testing of generic objects.

        The instance is callable with the following parameters:

        Parameters
        ----------
        - `data_to_snapshot` (`object`): The object data to be snapshotted.
        - `name` (`str`, optional): The name of the snapshot.
        - `filetype` (`str`, optional): The file type of the snapshot, by default "object.json".

        Returns
        -------
        ObjectExpect
        - `ObjectExpect`: The instance of the ObjectExpect class.

        Example
        -------
        `test_fixture_expect_object.py`
        ```python
        import pytest
        from snappylapy.fixtures import Expect

        def test_expect_object(expect: Expect) -> None:
            obj: dict[str, str] = {"key": "value"}
            expect.object(obj).to_match_snapshot()
        ```
        """

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

    def _read_snapshot(self) -> bytes:
        """Read the snapshot file."""
        return (self.settings.snapshot_dir / self.settings.filename).read_bytes()

    def _read_test_results(self) -> bytes:
        """Read the test results file."""
        return (self.settings.test_results_dir / self.settings.filename).read_bytes()


class LoadSnapshot:
    """
    Snapshot loading class.

    This class provides methods to load snapshots created by other tests.
    Each method loads and deserializes a specific type of snapshot.
    """

    def __init__(self, settings: Settings) -> None:
        """Do not initialize the LoadSnapshot class directly, should be used through the `load_snapshot` fixture in pytest."""  # noqa: E501
        self.settings = settings
        self._current_dependency_index = 0

    def _read_snapshot(self) -> bytes:
        """Read the snapshot file."""
        if self._current_dependency_index >= len(self.settings.depending_tests):
            msg = (
                f"Attempted to load more dependencies ({self._current_dependency_index + 1}) "
                f"than available ({len(self.settings.depending_tests)}). "
                "Check your test's dependency configuration."
            )
            raise IndexError(msg)
        if not self.settings.depending_tests[self._current_dependency_index].snapshots_base_dir:
            msg = "Depending snapshots base directory is not set."
            raise ValueError(msg)
        return (
            self.settings.depending_tests[self._current_dependency_index].snapshots_base_dir
            / DIRECTORY_NAMES.snapshot_dir_name
            / self.settings.depending_tests[self._current_dependency_index].filename
        ).read_bytes()

    def _load_and_deserialize(self, filename_extension: str, deserializer: Serializer[T]) -> T:
        """Set filename extension, read, deserialize, and increment dependency index."""
        self.settings.depending_tests[self._current_dependency_index].filename_extension = filename_extension
        deserialized_data = deserializer.deserialize(self._read_snapshot())
        self._current_dependency_index += 1
        return deserialized_data

    def dict(self) -> dict[Any, Any]:
        """
        Load dictionary snapshot.

        Use this method to load a dictionary snapshot that was created in a previous test.
        This is useful for reusing test data, isolating dependencies, and verifying integration between components.

        Example usage:
        --------------
        `test_load_snapshot_from_file_dict.py`
        ```python
        import pytest
        from snappylapy.fixtures import LoadSnapshot, Expect

        def create_dict() -> dict[str, int]:
            return {"apples": 3, "bananas": 5}

        def test_save_dict_snapshot(expect: Expect) -> None:
            data: dict[str, int] = create_dict()
            expect(data).to_match_snapshot()

        @pytest.mark.snappylapy(depends=[test_save_dict_snapshot])
        def test_load_snapshot_dict(load_snapshot: LoadSnapshot) -> None:
            data: dict[str, int] = load_snapshot.dict()
            assert data["apples"] == 3
            assert data["bananas"] == 5
        ```
        """
        return self._load_and_deserialize(
            "dict.json",
            JsonPickleSerializer[dict](),
        )

    def list(self) -> list[Any]:
        """
        Load list snapshot.

        Use this method to load a list snapshot that was created in a previous test.
        This is useful for reusing test data, isolating dependencies, and verifying integration between components.

        Example usage:
        --------------
        `test_load_snapshot_from_file_list.py`
        ```python
        import pytest
        from typing import Any
        from snappylapy import LoadSnapshot, Expect

        def transform_data(data: list) -> list:
            return [x * 2 for x in data]

        def next_transformation(data: list) -> list:
            return [x + 1 for x in data]

        def test_transform_data(expect: Expect) -> None:
            data = [1, 2, 3]
            result = transform_data(data)
            expect(result).to_match_snapshot()

        @pytest.mark.snappylapy(depends=[test_transform_data])
        def test_next_transformation(load_snapshot: LoadSnapshot, expect: Expect) -> None:
            data: list[Any] = load_snapshot.list()
            result = next_transformation(data)
            expect(result).to_match_snapshot()
        ```
        """
        return self._load_and_deserialize(
            "list.json",
            JsonPickleSerializer[list[Any]](),
        )

    def string(self) -> str:
        """
        Load string snapshot.

        Use this method to load a string snapshot that was created in a previous test.
        This is useful for reusing test data, isolating dependencies, and verifying integration between components.

        Example usage:
        --------------
        `test_load_snapshot_from_file_string.py`
        ```python
        import pytest
        from snappylapy.fixtures import LoadSnapshot, Expect

        def test_save_string_snapshot(expect: Expect) -> None:
            message: str = "Hello, pytest!"
            expect(message).to_match_snapshot()

        @pytest.mark.snappylapy(depends=[test_save_string_snapshot])
        def test_load_snapshot_string(load_snapshot: LoadSnapshot) -> None:
            data: str = load_snapshot.string()
            assert data == "Hello, pytest!"
        ```
        """
        return self._load_and_deserialize(
            "string.txt",
            StringSerializer(),
        )

    def bytes(self) -> bytes:
        r"""
        Load bytes snapshot.

        Use this method to load a bytes snapshot that was created in a previous test.
        This is useful for reusing test data, isolating dependencies, and verifying integration between components.

        Example usage:
        --------------
        `test_load_snapshot_from_file_bytes.py`
        ```python
        import pytest
        from snappylapy.fixtures import LoadSnapshot, Expect

        def test_save_bytes_snapshot(expect: Expect) -> None:
            data: bytes = b"\x01\x02\x03"
            expect(data).to_match_snapshot()

        @pytest.mark.snappylapy(depends=[test_save_bytes_snapshot])
        def test_load_snapshot_bytes(load_snapshot: LoadSnapshot) -> None:
            data: bytes = load_snapshot.bytes()
            assert data == b"\x01\x02\x03"
        ```
        """
        return self._load_and_deserialize(
            "bytes.txt",
            BytesSerializer(),
        )

    def dataframe(self) -> DataframeExpect.DataFrame:
        """
        Load dataframe snapshot.

        Use this method to load a dataframe snapshot that was created in a previous test.
        This is useful for reusing test data, isolating dependencies, and verifying integration between components.

        Example usage:
        --------------
        `test_load_snapshot_from_file_dataframe.py`
        ```python
        import pytest
        import pandas as pd
        from snappylapy.fixtures import LoadSnapshot, Expect

        def test_save_dataframe_snapshot(expect: Expect) -> None:
            df: pd.DataFrame = pd.DataFrame({"numbers": [1, 2, 3]})
            expect(df).to_match_snapshot()

        @pytest.mark.snappylapy(depends=[test_save_dataframe_snapshot])
        def test_load_snapshot_dataframe(load_snapshot: LoadSnapshot) -> None:
            df: pd.DataFrame = load_snapshot.dataframe()
            assert df["numbers"].sum() == 6
        ```
        """
        return self._load_and_deserialize(
            "dataframe.csv",
            PandasCsvSerializer(),
        )

    def object(self) -> object:
        """
        Load object snapshot.

        Use this method to load a generic object snapshot that was created in a previous test.
        This is useful for reusing test data, isolating dependencies, and verifying integration between components.

        Example usage:
        --------------
        `test_load_snapshot_from_file_object.py`
        ```python
        import pytest
        from snappylapy import Expect, LoadSnapshot

        class Custom:
            def __init__(self) -> None:
                self.value = 42

        def test_save_object_snapshot(expect: Expect) -> None:
            obj = Custom()
            expect(obj).to_match_snapshot()

        @pytest.mark.snappylapy(depends=[test_save_object_snapshot])
        def test_load_snapshot_object(load_snapshot: LoadSnapshot) -> None:
            obj = load_snapshot.object()
            assert hasattr(obj, "value")
            assert obj.value == 42
        ```
        """
        return self._load_and_deserialize(
            "object.json",
            JsonPickleSerializer[object](),
        )
