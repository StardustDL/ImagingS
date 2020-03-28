from typing import List
from ImagingS.core import Point
from . import Geometry


class Polygon(Geometry):
    def __init__(self, vertexes: List[Point]) -> None:
        super().__init__()
        self.vertexes = vertexes
