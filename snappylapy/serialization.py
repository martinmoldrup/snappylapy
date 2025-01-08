import json
from abc import ABC, abstractmethod
from typing import TypeVar, Generic
import jsonpickle

T = TypeVar('T')

class Serializer(ABC, Generic[T]):
    """Base class for serialization."""
    @abstractmethod
    def serialize(self, data: T) -> bytes:
        """Serialize data to bytes."""
        pass

    @abstractmethod
    def deserialize(self, data: bytes) -> T:
        """Deserialize bytes to data."""
        pass



class JsonSerializer(Serializer, Generic[T]):
    """Serialize and deserialize a dictionary."""
    def serialize(self, data: T) -> bytes:
        return json.dumps(data, default=str).encode()

    def deserialize(self, data: bytes) -> T:
        return json.loads(data)

class JsonPickleSerializer(Serializer, Generic[T]):
    """Serialize and deserialize a dictionary using pickle."""
    def serialize(self, data: T) -> bytes:
        json_string: str = jsonpickle.encode(data)
        return json_string.encode()

    def deserialize(self, data: bytes) -> T:
        return jsonpickle.decode(data)


class StringSerializer(Serializer[str]):
    """Serialize and deserialize a string."""
    def serialize(self, data: str) -> bytes:
        return data.encode()

    def deserialize(self, data: bytes) -> str:
        return data.decode()
    
class BytesSerializer(Serializer[bytes]):
    """Serialize and deserialize bytes."""
    def serialize(self, data: bytes) -> bytes:
        return data

    def deserialize(self, data: bytes) -> bytes:
        return data