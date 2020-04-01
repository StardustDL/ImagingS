from typing import List, Dict, Any
from ImagingS.core import Point, RectArea
from ImagingS.core.drawing import DrawingContext
from . import Geometry


class Polygon(Geometry):
    def __init__(self, vertexes: List[Point]) -> None:
        super().__init__()
        self.vertexes = vertexes
        self.algorithm = "DDA"

    def render(self, context: DrawingContext) -> None:
        raise NotImplementedError()

    def boundingArea(self, context: DrawingContext) -> RectArea:
        raise NotImplementedError()

    @staticmethod
    def deserialize(data: Dict) -> Any:
        raise NotImplementedError()
