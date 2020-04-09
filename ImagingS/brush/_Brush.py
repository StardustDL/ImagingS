from abc import ABC, abstractmethod

from ImagingS import Color, Point, Rect
from ImagingS.serialization import PropertySerializable


class Brush(PropertySerializable, ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def colorAt(self, position: Point, rect: Rect) -> Color: pass
