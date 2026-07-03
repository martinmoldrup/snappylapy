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
import enum
import typing
import dataclasses

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



class DataclassSerializer(Serializer[T], Generic[T]):
    """Serialize and deserialize dataclass instances using JSON, one level deep."""

    def serialize(self, data: T) -> bytes:
        """Serialize a dataclass instance to bytes, handling only one level deep."""
        if not dataclasses.is_dataclass(data):
            raise TypeError(f"Expected dataclass instance, got {type(data)}")

        result: dict[str, typing.Any] = {}
        for field in dataclasses.fields(data):
            value = getattr(data, field.name)
            if isinstance(value, enum.Enum):
                result[field.name] = value.value
            elif dataclasses.is_dataclass(value):
                # Only serialize one level deep: store as dict of its fields
                result[field.name] = self.serialize(value).decode(ENCODING_TO_USE)
            elif isinstance(value, (int, float, str, bool, type(None))):
                result[field.name] = value
            else:
                # For other types, use JsonPickleSerializer
                result[field.name] = JsonPickleSerializer().serialize(value).decode(ENCODING_TO_USE)

        json_string = json.dumps(
            result,
            indent=OUTPUT_JSON_INDENTATION_LEVEL,
            ensure_ascii=False,
        )
        json_string = json_string.replace("\r\n", "\n").replace("\r", "\n")
        return json_string.encode(encoding=ENCODING_TO_USE)

    def deserialize(self, data: bytes) -> T:
        """Deserialize bytes to a dataclass instance, handling only one level deep."""
        json_string: str = data.decode(ENCODING_TO_USE)
        obj_dict: dict[str, typing.Any] = json.loads(json_string)
        cls = typing.cast("type", type(self).__orig_bases__[0].__args__[0])  # type: ignore

        field_types: dict[str, type] = {f.name: f.type for f in dataclasses.fields(cls)}
        init_kwargs: dict[str, typing.Any] = {}

        for field_name, field_type in field_types.items():
            value = obj_dict.get(field_name)
            if value is None:
                init_kwargs[field_name] = None
            elif dataclasses.is_dataclass(field_type):
                # Deserialize nested dataclass one level deep
                init_kwargs[field_name] = DataclassSerializer[field_type]().deserialize(value.encode(ENCODING_TO_USE))
            elif isinstance(field_type, type) and issubclass(field_type, enum.Enum):
                init_kwargs[field_name] = field_type(value)
            elif field_type in (int, float, str, bool):
                init_kwargs[field_name] = value
            else:
                # For other types, use JsonPickleSerializer
                init_kwargs[field_name] = JsonPickleSerializer().deserialize(value.encode(ENCODING_TO_USE))

        return cls(**init_kwargs)
