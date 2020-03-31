from . import Brush
from ImagingS.core import Color, IdObject, Point, RectArea
from typing import Dict, Any


class Solid(Brush):
    def __init__(self, color: Color) -> None:
        super().__init__()
        self._color = color

    @property
    def color(self) -> Color:
        return self._color

    def color_at(self, position: Point, area: RectArea) -> Color:
        return self._color

    @staticmethod
    def deserialize(data: Dict) -> Any:
        result = Solid(data["_color"])
        IdObject.apply_id(result, data)
        return result
