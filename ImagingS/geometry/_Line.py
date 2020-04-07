from __future__ import annotations
from enum import IntEnum, unique

from typing import Iterable, Iterator, Optional

from ImagingS import Point, Rect
from ImagingS.drawing import Pen

from . import Geometry


@unique
class LineAlgorithm(IntEnum):
    Dda = 0
    Bresenham = 1


@unique
class LineClipAlgorithm(IntEnum):
    CohenSutherland = 0
    LiangBarsky = 1


class LineGeometry(Geometry):
    def __init__(self) -> None:
        super().__init__()
        self._start = Point()
        self.end = Point()
        self.algorithm = LineAlgorithm.Dda
        self.clip = None
        self.clip_algorithm = LineClipAlgorithm.CohenSutherland

    @staticmethod
    def create(start: Point, end: Point, algorithm: LineAlgorithm) -> LineGeometry:
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
    def algorithm(self) -> LineAlgorithm:
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value: LineAlgorithm) -> None:
        self._algorithm = value

    @property
    def clip(self) -> Optional[Rect]:
        return self._clip

    @clip.setter
    def clip(self, value: Optional[Rect]) -> None:
        self._clip = value

    @property
    def clip_algorithm(self) -> LineClipAlgorithm:
        return self._clip_algorithm

    @clip_algorithm.setter
    def clip_algorithm(self, value: LineClipAlgorithm) -> None:
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

    def stroke_points(self, pen: Pen) -> Iterable[Point]:
        start = self.start
        end = self.end
        if self.transform is not None:
            start = self.transform.transform(start)
            end = self.transform.transform(end)
        gen = self.__gen_DDA(start, end)
        if self.algorithm is LineAlgorithm.Dda:
            pass
        elif self.algorithm is LineAlgorithm.Bresenham:
            pass
        return gen

    def fill_points(self) -> Iterable[Point]:
        return []
