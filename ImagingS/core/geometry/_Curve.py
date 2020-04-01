from typing import List, Dict, Any
from ImagingS.core import Point, RectArea
from ImagingS.core.drawing import DrawingContext
from . import Geometry


class Curve(Geometry):
    def __init__(self, control_points: List[Point]) -> None:
        super().__init__()
        self.control_points = control_points
        self.algorithm = "Bezier"

    def render(self, context: DrawingContext) -> None:
        raise NotImplementedError()

    def boundingArea(self, context: DrawingContext) -> RectArea:
        raise NotImplementedError()

    @staticmethod
    def deserialize(data: Dict) -> Any:
        raise NotImplementedError()
