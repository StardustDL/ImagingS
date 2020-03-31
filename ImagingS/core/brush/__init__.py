from ImagingS.core import Color, Point, RectArea
from abc import ABC, abstractmethod
from ._Solid import Solid


class Brush(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def color_at(self, position: Point, area: RectArea) -> Color:
        pass


__all__ = (
    "Brush",
    "Solid"
)
