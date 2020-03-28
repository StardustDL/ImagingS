from ImagingS.core import Point, RectArea
from .drawing import Drawing
from typing import List


class Geometry(Drawing):
    def __init__(self) -> None:
        super().__init__()


class Line(Geometry):
    def __init__(self, start: Point, end: Point) -> None:
        super().__init__()
        self.start = start
        self.end = end
        self.algorithm = "DDA"


class Ellipse(Geometry):
    def __init__(self, area: RectArea) -> None:
        super().__init__()
        self.area = area


class Polygon(Geometry):
    def __init__(self, vertexes: List[Point]) -> None:
        super().__init__()
        self.vertexes = vertexes


class Curve(Geometry):
    def __init__(self, control_points: List[Point]) -> None:
        super().__init__()
        self.control_points = control_points
        self.algorithm = "Bezier"
