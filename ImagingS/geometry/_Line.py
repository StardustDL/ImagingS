from __future__ import annotations

from enum import IntEnum, unique
from typing import Iterable, Iterator, Optional

from ImagingS import Point, Rect, fsign
from ImagingS.drawing import Pen

from . import Geometry


@unique
class LineAlgorithm(IntEnum):
    Dda = 0
    Bresenham = 1


def _gen_DDA(start: Point, end: Point) -> Iterator[Point]:
    if start == end:
        yield start
        return
    xs, ys = map(round, start.as_tuple())
    xe, ye = map(round, end.as_tuple())
    dx, dy = xe-xs, ye-ys
    sx, sy = fsign(dx), fsign(dy)
    flag = False
    if abs(dy) > abs(dx):
        dx, dy = dy, dx
        flag = True
    k = dy / dx
    xc, yc = xs, ys
    for _ in range(round(abs(dx))+1):
        yield Point.create(xc, yc)
        if flag:
            yc += sy
            xc += k
        else:
            xc += sx
            yc += k


def _gen_Bresenham(start: Point, end: Point) -> Iterator[Point]:
    if start == end:
        yield start
        return
    xs, ys = map(round, start.as_tuple())
    xe, ye = map(round, end.as_tuple())
    dx, dy = xe-xs, ye-ys
    sx, sy = fsign(dx), fsign(dy)
    dx, dy = abs(dx), abs(dy)
    flag = False
    if dy > dx:
        dx, dy = dy, dx
        flag = True
    xc, yc = xs, ys
    ne = 2*dy-dx
    for _ in range(round(dx)+1):
        yield Point.create(xc, yc)
        if ne >= 0:
            if flag:
                xc += sx
            else:
                yc += sy
            ne -= 2*dx
        if flag:
            yc += sy
        else:
            xc += sx
        ne += 2*dy


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

    def stroke_points(self, pen: Pen) -> Iterable[Point]:
        start = self.start
        end = self.end
        if self.transform is not None:
            start = self.transform.transform(start)
            end = self.transform.transform(end)
        gen = None
        if self.algorithm is LineAlgorithm.Dda:
            gen = _gen_DDA
        elif self.algorithm is LineAlgorithm.Bresenham:
            gen = _gen_Bresenham
        return gen(start, end)

    def fill_points(self) -> Iterable[Point]:
        return []
