"""
Serialization classes for serializing and deserializing data.

Be sure that data is serialized the same way no matter what os and OS configuration is used.
"""
import json
import jsonpickle
from abc import ABC, abstractmethod
from io import StringIO
from snappylapy.constants import OUTPUT_JSON_INDENTATION_LEVEL
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    import pandas as pd

T = TypeVar("T")

ENCODING_TO_USE = "utf-8"


class Serializer(ABC, Generic[T]):
    """Base class for serialization."""

    @abstractmethod
    def serialize(self, data: T) -> bytes:
        """Serialize data to bytes."""

    @abstractmethod
    def deserialize(self, data: bytes) -> T:
        """Deserialize bytes to data."""


class JsonSerializer(Serializer, Generic[T]):
    """Serialize and deserialize a dictionary."""

    def serialize(self, data: T) -> bytes:
        """Serialize a dictionary to bytes with cross-platform consistency."""
        json_string = json.dumps(
            data,
            default=str,
            indent=OUTPUT_JSON_INDENTATION_LEVEL,
            ensure_ascii=False,
        )
        json_string = json_string.replace("\r\n", "\n").replace("\r", "\n")  # Normalize all line endings to LF
        return json_string.encode(encoding=ENCODING_TO_USE)

    def deserialize(self, data: bytes) -> T:
        """Deserialize bytes to a dictionary."""
        return json.loads(data.decode(encoding=ENCODING_TO_USE))


class JsonPickleSerializer(Serializer, Generic[T]):
    """Serialize and deserialize a dictionary using pickle."""

    def serialize(self, data: T) -> bytes:
        """Serialize a dictionary/list or other to bytes in json format with cross-platform consistency."""
        json_string: str = jsonpickle.encode(
            data,
            indent=OUTPUT_JSON_INDENTATION_LEVEL,
            make_refs=False,
        )
        json_string = json_string.replace("\r\n", "\n").replace("\r", "\n")  # Normalize all line endings to LF
        return json_string.encode(encoding=ENCODING_TO_USE)

    def deserialize(self, data: bytes) -> T:
        """Deserialize bytes to a dictionary or list."""
        return jsonpickle.decode(data.decode(encoding=ENCODING_TO_USE))  # noqa: S301, pickle security, data should be trusted here, keep your snapshot files safe


class StringSerializer(Serializer[str]):
    """Serialize and deserialize a string."""

    def serialize(self, data: str) -> bytes:
        """Serialize a string to bytes."""
        return data.encode(encoding=ENCODING_TO_USE)

    def deserialize(self, data: bytes) -> str:
        """Deserialize bytes to a string."""
        return data.decode(encoding=ENCODING_TO_USE)


class BytesSerializer(Serializer[bytes]):
    """Serialize and deserialize bytes."""

    def serialize(self, data: bytes) -> bytes:
        """Already in bytes, return as is."""
        return data

    def deserialize(self, data: bytes) -> bytes:
        """Already in bytes, return as is."""
        return data


class PandasCsvSerializer(Serializer["pd.DataFrame"]):
    """Serialize and deserialize pandas DataFrames using CSV format."""

    def serialize(self, data: "pd.DataFrame") -> bytes:
        """Serialize a pandas DataFrame to bytes using CSV format."""
        try:
            # Lazy import to avoid dependency issues if pandas is not installed
            import pandas as pd  # noqa: F401, PLC0415
        except ImportError as e:
            msg = "pandas is required for DataFrame serialization"
            raise ImportError(msg) from e

        if not hasattr(data, "to_csv"):
            msg = f"Expected pandas DataFrame, got {type(data)}"
            raise TypeError(msg)

        # Use StringIO to capture CSV output
        csv_buffer = StringIO()
        data.to_csv(csv_buffer, index=True, lineterminator="\n")
        csv_string = csv_buffer.getvalue()

        # Ensure consistent line endings
        csv_string = csv_string.replace("\r\n", "\n").replace("\r", "\n")
        return csv_string.encode(encoding=ENCODING_TO_USE)

    def deserialize(self, data: bytes) -> "pd.DataFrame":
        """Deserialize bytes to a pandas DataFrame."""
        try:
            # Lazy import to avoid dependency issues if pandas is not installed
            import pandas as pd  # noqa: PLC0415
        except ImportError as e:
            msg = "pandas is required for DataFrame deserialization"
            raise ImportError(msg) from e

        csv_string = data.decode(encoding=ENCODING_TO_USE)

        # Use StringIO to read CSV data
        csv_buffer = StringIO(csv_string)
        dataframe = pd.read_csv(csv_buffer, index_col=0)
        return dataframe
