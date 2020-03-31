from abc import ABC, abstractmethod
from typing import Any, Dict


class Serializable(ABC):
    def __init__(self) -> None:
        super().__init__()

    def serialize(self) -> Dict:
        return self.__dict__

    @staticmethod
    @abstractmethod
    def deserialize(data: Dict) -> Any:
        pass
