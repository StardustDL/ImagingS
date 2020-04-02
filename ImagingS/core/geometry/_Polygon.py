from __future__ import annotations
from typing import List
from ImagingS.core import Point, RectArea
from ImagingS.core.drawing import DrawingContext
from . import Geometry


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

    def render(self, context: DrawingContext) -> None:
        raise NotImplementedError()

    @property
    def boundingArea(self) -> RectArea:
        raise NotImplementedError()
