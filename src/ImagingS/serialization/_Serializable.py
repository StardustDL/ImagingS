from abc import ABC, abstractmethod
from typing import Dict

from . import getProperties


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
        for prop in getProperties(self):
            if prop.canSet:
                result[prop.name] = prop.get()
        return result

    def deserialize(self, data: Dict) -> None:
        for prop in getProperties(self):
            if prop.canSet and prop.name in data:
                value = data[prop.name]
                prop.set(value)
                # if isinstance(value, prop.data_type):
                # else:
                # raise Exception(f"Error type cast: {value.__class__} != {prop.data_type}")
