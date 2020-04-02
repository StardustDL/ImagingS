from __future__ import annotations
from typing import Iterator
from ImagingS.core import Point, RectArea
from ImagingS.core.drawing import DrawingContext
from . import Geometry


class Line(Geometry):
    def __init__(self) -> None:
        super().__init__()
        self._start = Point()
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
        self.__update_bounding_area()

    @property
    def end(self) -> Point:
        return self._end

    @end.setter
    def end(self, value: Point) -> None:
        self._end = value
        self.__update_bounding_area()

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

    def __gen_DDA(self) -> Iterator[Point]:
        delta = self.end - self.start
        lx, ly = abs(delta.x), abs(delta.y)
        le = min(lx, ly)
        if le < 1e-8:
            le = max(lx, ly)
        if le < 1:
            le = 1
        le = round(le)
        delta.x /= le
        delta.y /= le
        cur = self.start
        for _ in range(le + 1):
            yield cur
            cur = cur + delta

    def render(self, context: DrawingContext) -> None:
        gen = self.__gen_DDA
        if self.algorithm == "DDA":
            pass
        elif self.algorithm == "Bresenham":
            pass
        for p in gen():
            rp = p
            if self.transform is not None:
                rp = self.transform.transform(p)
            if rp:
                context.point(rp, self.stroke.color_at(rp, self.boundingArea))

    @property
    def boundingArea(self) -> RectArea:
        return self._bounding_area

    def __update_bounding_area(self):
        x0, y0 = self.start.as_tuple()
        x1, y1 = self.end.as_tuple()

        x = min(x0, x1)
        y = min(y0, y1)
        x2 = max(x0, x1)
        y2 = max(y0, y1)
        self._bounding_area = RectArea.from_points(
            Point.create(x, y), Point.create(x2, y2))
