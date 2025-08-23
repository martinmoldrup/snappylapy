"""
Serialization classes for serializing and deserializing data.

Be sure that data is serialized the same way no matter what os and OS configuration is used.
"""
import json
import jsonpickle
from abc import ABC, abstractmethod
from snappylapy.constants import OUTPUT_JSON_INDENTATION_LEVEL
from typing import Generic, TypeVar

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
