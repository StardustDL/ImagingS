from __future__ import annotations
from typing import List
from ImagingS.core import Point, RectArea
from ImagingS.core.drawing import DrawingContext
from . import Geometry, Line


class Polygon(Geometry):
    def __init__(self) -> None:
        super().__init__()
        self.vertexes = []
        self.algorithm = "DDA"

    @staticmethod
    def create(vertexes: List[Point], algorithm: str) -> Polygon:
        result = Polygon()
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
        self.__update_bounding_area()

    def render(self, context: DrawingContext) -> None:
        cnt = len(self.vertexes)
        if cnt == 0:
            return
        for i in range(cnt):
            j = (i+1) % cnt
            ln = Line.create(self.vertexes[i],
                             self.vertexes[j], self.algorithm)
            ln.stroke = self.stroke
            ln.transform = self.transform
            ln.render(context)

    @property
    def boundingArea(self) -> RectArea:
        return self._bounding_area
    
    def __update_bounding_area(self):
        if len(self.vertexes) == 0:
            self._bounding_area = RectArea()
            return
        xn, yn = self.vertexes[0].as_tuple()
        xx, yx = xn, yn
        for p in self.vertexes:
            tx, ty = p.as_tuple()
            xn, yn = min(xn, tx), min(yn, ty)
            xx, yx = max(xx, tx), max(yx, ty)
        self._bounding_area = RectArea.from_points(Point.create(xn, yn), Point.create(xx, yx))
