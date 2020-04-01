from ImagingS.core import Color, Point, RectArea
from ImagingS.core.serialization import Serializable
from abc import ABC, abstractmethod
from typing import Dict, Any


class Brush(Serializable, ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def color_at(self, position: Point, area: RectArea) -> Color:
        pass

    @staticmethod
    @abstractmethod
    def deserialize(data: Dict) -> Any:
        pass
