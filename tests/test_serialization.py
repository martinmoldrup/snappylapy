"""Test cases for serialization module."""
from snappylapy.serialization import StringSerializer, JsonSerializer, JsonPickleSerializer
from datetime import datetime
import pytest

def test_string_serializer_serialize():
    """Test serialization of a string."""
    serializer = StringSerializer()
    data = "hello"
    serialized_data = serializer.serialize(data)
    assert serialized_data == b"hello"

def test_string_serializer_deserialize():
    """Test deserialization of bytes to string."""
    serializer = StringSerializer()
    data = b"hello"
    deserialized_data = serializer.deserialize(data)
    assert deserialized_data == "hello"

def test_string_serializer_round_trip():
    """Test round-trip serialization and deserialization."""
    serializer = StringSerializer()
    data = "hello"
    serialized_data = serializer.serialize(data)
    deserialized_data = serializer.deserialize(serialized_data)
    assert deserialized_data == data
   

def test_json_serializer_serialize():
    """Test serialization of a dictionary."""
    serializer = JsonSerializer[dict]()
    data = {"key": "value"}
    serialized_data = serializer.serialize(data)
    assert serialized_data == b'{\n  "key": "value"\n}'

def test_json_serializer_deserialize():
    """Test deserialization of bytes to dictionary."""
    serializer = JsonSerializer[dict]()
    data = b'{"key": "value"}'
    deserialized_data = serializer.deserialize(data)
    assert deserialized_data == {'key': 'value'}

def test_json_serializer_round_trip():
    """Test round-trip serialization and deserialization."""
    serializer = JsonSerializer[dict]()
    data = {"key": "value"}
    serialized_data = serializer.serialize(data)
    deserialized_data = serializer.deserialize(serialized_data)
    assert deserialized_data == data

def test_json_serializer_nested_dict():
    """Test serialization of a nested dictionary."""
    serializer = JsonSerializer[dict]()
    data = {"key": {"nested_key": "nested_value"}}
    serialized_data = serializer.serialize(data)
    assert serialized_data == b'{\n  "key": {\n    "nested_key": "nested_value"\n  }\n}'
    deserialized_data = serializer.deserialize(serialized_data)
    assert deserialized_data == data

# jsonpickle

def test_jsonpickle_serializer_serialize():
    """Test serialization of a dictionary."""
    serializer = JsonPickleSerializer[dict]()
    data = {"key": "value"}
    serialized_data = serializer.serialize(data)
    assert serialized_data == b'{\n  "key": "value"\n}'

def test_jsonpickle_serializer_deserialize():
    """Test deserialization of bytes to dictionary."""
    serializer = JsonPickleSerializer[dict]()
    data = b'{"key": "value"}'
    deserialized_data = serializer.deserialize(data)
    assert deserialized_data == {"key": "value"}

def test_jsonpickle_serializer_round_trip():
    """Test round-trip serialization and deserialization."""
    serializer = JsonPickleSerializer[dict]()
    data = {"key": "value"}
    serialized_data = serializer.serialize(data)
    deserialized_data = serializer.deserialize(serialized_data)
    assert deserialized_data == data

class CustomObject:
    def __init__(self, name: str, value: int) -> None:
        """Initialize CustomObject with name and value."""
        self.name: str = name
        self.value: int = value

    def get_string(self) -> str:
        """Return a string representation of the object."""
        var = 234
        return f"{self.name} - {self.value} - {var}"


def test_jsonpickle_serializer_nested_dict():
    """Test serialization of a nested dictionary."""
    serializer = JsonPickleSerializer[dict]()
    data = {"key": {"nested_key": "nested_value"}}
    serialized_data = serializer.serialize(data)
    assert serialized_data == b'{\n  "key": {\n    "nested_key": "nested_value"\n  }\n}'
    deserialized_data = serializer.deserialize(serialized_data)
    assert deserialized_data == data


def test_jsonpickle_serializer_datetime():
    """Test serialization of a dictionary with datetime object."""
    serializer = JsonPickleSerializer[dict]()
    now = datetime.now()
    data = {"timestamp": now}
    serialized_data = serializer.serialize(data)
    # assert serialized_data == f'{{"timestamp": "{str(now)}"}}'.encode()
    deserialized_data = serializer.deserialize(serialized_data)
    assert deserialized_data == data


def test_jsonpickle_serializer_custom_object():
    """Test serialization of a custom object."""
    serializer = JsonPickleSerializer[dict]()
    obj = CustomObject(name="test", value=123)
    data = {"obj": obj}
    serialized_data = serializer.serialize(data)
    # assert serialized_data == b'{"name": "test", "value": 123}'
    deserialized_data = serializer.deserialize(serialized_data)

    assert isinstance(deserialized_data["obj"], CustomObject)
    assert deserialized_data["obj"].name == "test"
    assert deserialized_data["obj"].value == 123
    assert deserialized_data["obj"].get_string() == "test - 123 - 234"