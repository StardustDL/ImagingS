from __future__ import annotations

from enum import Enum, unique
from typing import Iterable, Iterator, Optional, cast

from ImagingS import Point, Rect, fsign
from ImagingS.drawing import Pen

from . import Geometry


@unique
class LineAlgorithm(Enum):
    Dda = 0
    Bresenham = 1


@unique
class LineClipAlgorithm(Enum):
    CohenSutherland = 0
    LiangBarsky = 1


def _genDDA(start: Point, end: Point) -> Iterator[Point]:
    if start == end:
        yield start
        return
    xs, ys = map(round, start.asTuple())
    xe, ye = map(round, end.asTuple())
    dx, dy = xe-xs, ye-ys
    sx, sy = fsign(dx), fsign(dy)
    dx, dy = abs(dx), abs(dy)
    flag = False
    if dy > dx:
        dx, dy = dy, dx
        flag = True
    k = dy / dx
    if flag:
        k *= sx
    else:
        k *= sy
    xc, yc = xs, ys
    for _ in range(round(abs(dx))+1):
        yield Point(xc, yc)
        if flag:
            yc += sy
            xc += k
        else:
            xc += sx
            yc += k


def _genBresenham(start: Point, end: Point) -> Iterator[Point]:
    if start == end:
        yield start
        return
    xs, ys = map(round, start.asTuple())
    xe, ye = map(round, end.asTuple())
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
        yield Point(xc, yc)
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


class LineGeometry(Geometry):
    def __init__(self, start: Optional[Point] = None, end: Optional[Point] = None, algorithm: Optional[LineAlgorithm] = None) -> None:
        super().__init__()
        self.start = start if start else Point()
        self.end = end if end else Point()
        self.algorithm = algorithm if algorithm else LineAlgorithm.Dda

    @property
    def start(self) -> Point:
        return self._start

    @start.setter
    def start(self, value: Point) -> None:
        assert isinstance(value, Point)
        self._start = value
        self.refreshBounds()

    @property
    def end(self) -> Point:
        return self._end

    @end.setter
    def end(self, value: Point) -> None:
        assert isinstance(value, Point)
        self._end = value
        self.refreshBounds()

    @property
    def algorithm(self) -> LineAlgorithm:
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value: LineAlgorithm) -> None:
        assert isinstance(value, LineAlgorithm)
        self._algorithm = value

    def transformed(self) -> Geometry:
        if self.transform is None:
            return self
        else:
            start = self.transform.transform(self.start)
            end = self.transform.transform(self.end)
            return LineGeometry(start, end, self.algorithm)

    def strokePoints(self, pen: Pen) -> Iterable[Point]:
        target = self
        if self.transform is not None:
            target = cast(LineGeometry, self.transformed())

        gen = None
        if target.algorithm is LineAlgorithm.Dda:
            gen = _genDDA
        elif target.algorithm is LineAlgorithm.Bresenham:
            gen = _genBresenham
        return gen(target.start, target.end)

    def fillPoints(self) -> Iterable[Point]:
        return []

    def _calculateBounds(self) -> Rect:
        target = self
        if self.transform is not None:
            target = cast(LineGeometry, self.transformed())
        return Rect.fromPoints(target.start, target.end)
