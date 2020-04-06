from abc import ABC, abstractmethod

from ImagingS.core import Color, Point, Rect
from ImagingS.core.serialization import PropertySerializable


class Brush(PropertySerializable, ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def color_at(self, position: Point, area: Rect) -> Color:
        pass
