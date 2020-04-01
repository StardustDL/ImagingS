from ImagingS.core import Point, RectArea
from ImagingS.core.drawing import DrawingContext
from typing import Dict, Any
from . import Geometry


class Line(Geometry):
    def __init__(self, start: Point, end: Point) -> None:
        super().__init__()
        self.start = start
        self.end = end
        self.algorithm = "DDA"

    def render(self, context: DrawingContext) -> None:
        raise NotImplementedError()

    def boundingArea(self, context: DrawingContext) -> RectArea:
        raise NotImplementedError()

    @staticmethod
    def deserialize(data: Dict) -> Any:
        raise NotImplementedError()
