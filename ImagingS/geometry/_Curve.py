from __future__ import annotations

from typing import Iterable, List

from ImagingS import Point
from ImagingS.drawing import Pen

from . import Geometry


class CurveGeometry(Geometry):
    def __init__(self, ) -> None:
        super().__init__()
        self.control_points = []
        self.algorithm = "Bezier"

    @staticmethod
    def create(control_points: List[Point], algorithm: str) -> CurveGeometry:
        result = CurveGeometry()
        result.control_points = control_points
        result.algorithm = algorithm
        return result

    @property
    def control_points(self) -> List[Point]:
        return self._control_points

    @control_points.setter
    def control_points(self, value: List[Point]) -> None:
        self._control_points = value

    @property
    def algorithm(self) -> str:
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value: str) -> None:
        self._algorithm = value

    def stroke_points(self, pen: Pen) -> Iterable[Point]:
        return []

    def fill_points(self) -> Iterable[Point]:
        return []
