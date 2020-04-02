from __future__ import annotations
from ImagingS.core import Point, RectArea, Size
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

    def __update_bounding_area(self):
        x0, y0 = int(self.start.x), int(self.start.y)
        x1, y1 = int(self.end.x), int(self.end.y)
        x = min(x0, x1)
        y = min(y0, y1)
        w = max(x0, x1) - x
        h = max(y0, y1) - y
        self._bounding_area = RectArea.create(
            Point.create(x, y), Size.create(w, h))

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

    def render(self, context: DrawingContext) -> None:
        def points():
            x0, y0 = int(self.start.x), int(self.start.y)
            x1, y1 = int(self.end.x), int(self.end.y)
            if x0 == x1:
                for y in range(y0, y1 + 1):
                    yield Point.create(x0, y)
            else:
                if x0 > x1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                k = (y1 - y0) / (x1 - x0)
                for x in range(x0, x1 + 1):
                    yield Point.create(x, int(y0 + k * (x - x0)))

        for p in points():
            context.point(p, self.stroke.color_at(p, self.boundingArea))

    @property
    def boundingArea(self) -> RectArea:
        return self._bounding_area
