from __future__ import annotations
from typing import Iterator, Optional, Iterable
from ImagingS.core import Point, Rect
from ImagingS.core.drawing import Pen
from . import Geometry


class LineGeometry(Geometry):
    def __init__(self) -> None:
        super().__init__()
        self._start = Point()
        self.end = Point()
        self.algorithm = "DDA"
        self.clip = None
        self.clip_algorithm = "Cohen-Sutherland"

    @staticmethod
    def create(start: Point, end: Point, algorithm: str) -> LineGeometry:
        result = LineGeometry()
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

    @property
    def clip(self) -> Optional[Rect]:
        return self._clip

    @clip.setter
    def clip(self, value: Optional[Rect]) -> None:
        self._clip = value

    @property
    def clip_algorithm(self) -> str:
        return self._clip_algorithm

    @clip_algorithm.setter
    def clip_algorithm(self, value: str) -> None:
        self._clip_algorithm = value

    @staticmethod
    def __gen_DDA(start: Point, end: Point) -> Iterator[Point]:
        delta = end - start
        lx, ly = abs(delta.x), abs(delta.y)
        le = min(lx, ly)
        if le < 1e-8:
            le = max(lx, ly)
        if le < 1:
            le = 1
        le = round(le)
        delta.x /= le
        delta.y /= le
        cur = start
        for _ in range(le + 1):
            yield cur
            cur = cur + delta

    # def render(self, context: DrawingContext) -> None:
    #     start = self.start
    #     end = self.end
    #     if self.transform is not None:
    #         start = self.transform.transform(start)
    #         end = self.transform.transform(end)
    #     gen = self.__gen_DDA(start, end)
    #     if self.algorithm == "DDA":
    #         pass
    #     elif self.algorithm == "Bresenham":
    #         pass
    #     for p in gen:
    #         if p in context.area():
    #             context.point(p, self.stroke.color_at(p, self.boundingArea))

    def stroke_points(self, pen: Pen) -> Iterable[Point]:
        raise NotImplementedError()

    def fill_points(self) -> Iterable[Point]:
        raise NotImplementedError()

    def in_stroke(self, pen: Pen, point: Point) -> bool:
        raise NotImplementedError()

    def in_fill(self, point: Point) -> bool:
        raise NotImplementedError()
