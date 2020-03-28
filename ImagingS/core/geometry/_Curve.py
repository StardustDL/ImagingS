from typing import List
from ImagingS.core import Point
from . import Geometry


class Curve(Geometry):
    def __init__(self, control_points: List[Point]) -> None:
        super().__init__()
        self.control_points = control_points
        self.algorithm = "Bezier"
