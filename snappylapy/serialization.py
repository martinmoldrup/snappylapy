"""Serialization classes for serializing and deserializing data."""
import json
import jsonpickle
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


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
        """Serialize a dictionary to bytes."""
        return json.dumps(data, default=str).encode()

    def deserialize(self, data: bytes) -> T:
        """Deserialize bytes to a dictionary."""
        return json.loads(data)


class JsonPickleSerializer(Serializer, Generic[T]):
    """Serialize and deserialize a dictionary using pickle."""

    def serialize(self, data: T) -> bytes:
        """Serialize a dictionary/list or other to bytes in json format."""
        json_string: str = jsonpickle.encode(data)
        return json_string.encode()

    def deserialize(self, data: bytes) -> T:
        """Deserialize bytes to a dictionary or list."""
        return jsonpickle.decode(data)  # noqa: S301, pickle security, data should be trusted here, keep your snapshot files safe


class StringSerializer(Serializer[str]):
    """Serialize and deserialize a string."""

    def serialize(self, data: str) -> bytes:
        """Serialize a string to bytes."""
        return data.encode()

    def deserialize(self, data: bytes) -> str:
        """Deserialize bytes to a string."""
        return data.decode()


class BytesSerializer(Serializer[bytes]):
    """Serialize and deserialize bytes."""

    def serialize(self, data: bytes) -> bytes:
        """Already in bytes, return as is."""
        return data

    def deserialize(self, data: bytes) -> bytes:
        """Already in bytes, return as is."""
        return data
