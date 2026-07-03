"""This is to test if complex dataclasses can be created and inverted, for instance nested dataclasses and dataclasses containing enums or custom types."""
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass, asdict

@dataclass
class InnerDataClass:
    id: int
    name: str

class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

@dataclass
class ComplexDataClass:
    inner: InnerDataClass
    status: Status
    tags: List[str]
    optional_field: Optional[float] = None

class_instance = ComplexDataClass(
    inner=InnerDataClass(id=1, name="Test"),
    status=Status.ACTIVE,
    tags=["tag1", "tag2"],
    optional_field=3.14
)

# Convert dataclass instance to dictionary
dict_representation = asdict(class_instance)
print("Dictionary Representation:", dict_representation)

# Convert dictionary back to dataclass instance
reconstructed_instance = ComplexDataClass(**dict_representation)
print("Reconstructed Instance:", reconstructed_instance)
