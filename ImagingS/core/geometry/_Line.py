from __future__ import annotations
from ImagingS.core import Point, RectArea
from ImagingS.core.drawing import DrawingContext
from . import Geometry


class Line(Geometry):
    def __init__(self) -> None:
        super().__init__()
        self.start = Point()
        self.end = Point()
        self.algorithm = "DDA"

    @staticmethod
    def create(start: Point, end: Point, algorithm: str) -> Line:
        result = Line()
        result.start = start
        result.end = end
        result.algorithm = algorithm
        return result

    @property
    def start(self) -> Point:
        return self._start

    @start.setter
    def start(self, value: Point) -> None:
        self._start = value

    @property
    def end(self) -> Point:
        return self._end

    @end.setter
    def end(self, value: Point) -> None:
        self._end = value

    @property
    def algorithm(self) -> str:
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value: str) -> None:
        self._algorithm = value

    @property
    def algorithm(self) -> str:
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value: str) -> None:
        self._algorithm = value

    def render(self, context: DrawingContext) -> None:
        raise NotImplementedError()

    def boundingArea(self, context: DrawingContext) -> RectArea:
        raise NotImplementedError()
