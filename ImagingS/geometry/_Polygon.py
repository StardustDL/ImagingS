from __future__ import annotations

from typing import Iterable, List

from ImagingS import Point
from ImagingS.drawing import Pen

from . import Geometry, LineGeometry, LineAlgorithm


class PolygonGeometry(Geometry):
    S_Vertexes = "vertexes"

    def __init__(self) -> None:
        super().__init__()
        self.vertexes = []
        self.algorithm = LineAlgorithm.Dda

    @staticmethod
    def create(vertexes: List[Point], algorithm: LineAlgorithm) -> PolygonGeometry:
        result = PolygonGeometry()
        result.vertexes = vertexes
        result.algorithm = algorithm
        return result

    @property
    def algorithm(self) -> LineAlgorithm:
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value: LineAlgorithm) -> None:
        self._algorithm = value

    @property
    def vertexes(self) -> List[Point]:
        return self._vertexes

    @vertexes.setter
    def vertexes(self, value: List[Point]) -> None:
        self._vertexes = value

    def stroke_points(self, pen: Pen) -> Iterable[Point]:
        cnt = len(self.vertexes)
        if cnt == 0:
            return
        for i in range(cnt):
            j = (i+1) % cnt
            ln = LineGeometry.create(self.vertexes[i],
                                     self.vertexes[j], self.algorithm)
            ln.transform = self.transform
            for point in ln.stroke_points(pen):
                yield point

    def fill_points(self) -> Iterable[Point]:
        return []
