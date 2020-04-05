from __future__ import annotations
from typing import List, Iterable
from ImagingS.core import Point
from ImagingS.core.drawing import Pen
from . import Geometry, LineGeometry


class PolygonGeometry(Geometry):
    S_Vertexes = "vertexes"

    def __init__(self) -> None:
        super().__init__()
        self.vertexes = []
        self.algorithm = "DDA"

    @staticmethod
    def create(vertexes: List[Point], algorithm: str) -> PolygonGeometry:
        result = PolygonGeometry()
        result.vertexes = vertexes
        result.algorithm = algorithm
        return result

    @property
    def algorithm(self) -> str:
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value: str) -> None:
        self._algorithm = value

    @property
    def vertexes(self) -> List[Point]:
        return self._vertexes

    @vertexes.setter
    def vertexes(self, value: List[Point]) -> None:
        self._vertexes = value

    # def render(self, context: DrawingContext) -> None:
    #     cnt = len(self.vertexes)
    #     if cnt == 0:
    #         return
    #     for i in range(cnt):
    #         j = (i+1) % cnt
    #         ln = Line.create(self.vertexes[i],
    #                          self.vertexes[j], self.algorithm)
    #         ln.stroke = self.stroke
    #         ln.transform = self.transform
    #         ln.render(context)

    def stroke_points(self, pen: Pen) -> Iterable[Point]:
        raise NotImplementedError()

    def fill_points(self) -> Iterable[Point]:
        raise NotImplementedError()

    def in_stroke(self, pen: Pen, point: Point) -> bool:
        raise NotImplementedError()

    def in_fill(self, point: Point) -> bool:
        raise NotImplementedError()
