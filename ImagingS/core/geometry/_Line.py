from ImagingS.core import Point
from . import Geometry


class Line(Geometry):
    def __init__(self, start: Point, end: Point) -> None:
        super().__init__()
        self.start = start
        self.end = end
        self.algorithm = "DDA"
