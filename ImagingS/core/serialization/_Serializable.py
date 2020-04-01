from abc import ABC, abstractmethod
from typing import Dict
from . import get_properties


class Serializable(ABC):
    @abstractmethod
    def serialize(self) -> Dict:
        pass

    @abstractmethod
    def deserialize(self, data: Dict) -> None:
        pass


class PropertySerializable(Serializable):
    def serialize(self) -> Dict:
        result = {}
        for prop in get_properties(self):
            if prop.can_set:
                result[prop.name] = prop.get()
        return result

    def deserialize(self, data: Dict) -> None:
        for prop in get_properties(self):
            if prop.can_set and prop.name in data:
                value = data[prop.name]
                prop.set(value)
                # if isinstance(value, prop.data_type):
                # else:
                # raise Exception(f"Error type cast: {value.__class__} != {prop.data_type}")
