from __future__ import annotations

from enum import Enum, unique
from typing import Iterable, Iterator, Optional, Tuple, cast

from ImagingS import Point, Rect, fsign
from ImagingS.drawing import Pen

from . import Geometry


@unique
class LineAlgorithm(Enum):
    Dda = 0
    Bresenham = 1


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


def _clipCohenSutherland(start: Point, end: Point, area: Rect) -> Optional[Tuple[Point, Point]]:
    if start == end:
        if start in area:
            return start, end
        else:
            return None
    aori, aver = area.origin, area.vertex
    LEFT, RIGHT, BOTTOM, TOP = 1, 2, 4, 8

    def encodePoint(p: Point) -> int:
        res = 0
        if p.x < aori.x:
            res |= LEFT
        elif p.x > aver.x:
            res |= RIGHT
        if p.y < aori.y:
            res |= BOTTOM
        elif p.y > aver.y:
            res |= TOP
        return res

    p0, p1 = start.clone(), end.clone()
    c0, c1 = encodePoint(p0), encodePoint(p1)
    while c0 != 0 or c1 != 0:
        if (c0 & c1) != 0:
            return None
        c = c0 if c0 != 0 else c1
        pt = Point()
        if (LEFT & c) != 0:
            pt = Point(aori.x, p0.y + (p1.y - p0.y) * (aori.x - p0.x) / (p1.x - p0.x))
        elif (RIGHT & c) != 0:
            pt = Point(aver.x, p0.y + (p1.y - p0.y) * (aver.x - p0.x) / (p1.x - p0.x))
        elif (BOTTOM & c) != 0:
            pt = Point(p0.x + (p1.x - p0.x) * (aori.y - p0.y) / (p1.y - p0.y), aori.y)
        elif (TOP & c) != 0:
            pt = Point(p0.x + (p1.x - p0.x) * (aver.y - p0.y) / (p1.y - p0.y), aver.y)
        else:
            assert False  # not full zero
        if c == c0:
            p0 = pt
            c0 = encodePoint(p0)
        else:
            p1 = pt
            c1 = encodePoint(p1)
    return p0, p1


def _clipLiangBarsky(start: Point, end: Point, area: Rect) -> Optional[Tuple[Point, Point]]:
    if start == end:
        if start in area:
            return start, end
        else:
            return None
    aori, aver = area.origin, area.vertex
    EPS = 1e-5

    def clipTest(a: float, b: float, t0: float, t1: float) -> Optional[Tuple[float, float]]:
        flag = True
        r0, r1 = t0, t1
        if a < -EPS:
            t = b/a
            if t > t1:
                flag = False
            elif t > t0:
                r0 = t
        elif a > EPS:
            t = b/a
            if t < t0:
                flag = False
            elif t < t1:
                r1 = t
        elif b < 0:
            flag = False
        return (r0, r1) if flag else None

    t0, t1 = 0.0, 1.0
    x0, y0 = start.asTuple()
    x1, y1 = end.asTuple()
    dx, dy = end.x - start.x, end.y - start.y

    res = clipTest(-dx, x0 - aori.x, t0, t1)
    if res is None:
        return None
    t0, t1 = res

    res = clipTest(dx, aver.x - x0, t0, t1)
    if res is None:
        return None
    t0, t1 = res

    res = clipTest(-dy, y0 - aori.y, t0, t1)
    if res is None:
        return None
    t0, t1 = res

    res = clipTest(dy, aver.y - y0, t0, t1)
    if res is None:
        return None
    t0, t1 = res

    if t1 < 1:
        x1, y1 = x0 + t1 * dx, y0 + t1 * dy
    if t0 > 0:
        x0, y0 = x0 + t0 * dx, y0 + t0 * dy

    return Point(x0, y0), Point(x1, y1)


@unique
class LineClipAlgorithm(Enum):
    CohenSutherland = 0
    LiangBarsky = 1


class LineGeometry(Geometry):
    def __init__(self, start: Optional[Point] = None, end: Optional[Point] = None, algorithm: Optional[LineAlgorithm] = None) -> None:
        super().__init__()
        self.start = start if start else Point()
        self.end = end if end else Point()
        self.algorithm = algorithm if algorithm else LineAlgorithm.Dda
        self.clip = None
        self.clipAlgorithm = LineClipAlgorithm.CohenSutherland

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

    @property
    def clip(self) -> Optional[Rect]:
        return self._clip

    @clip.setter
    def clip(self, value: Optional[Rect]) -> None:
        self._clip = value

    @property
    def clipAlgorithm(self) -> LineClipAlgorithm:
        return self._clipAlgorithm

    @clipAlgorithm.setter
    def clipAlgorithm(self, value: LineClipAlgorithm) -> None:
        self._clipAlgorithm = value

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

        # line clip special begin

        if self.clip is not None:
            cliped = None
            if self.clipAlgorithm is LineClipAlgorithm.CohenSutherland:
                cliped = _clipCohenSutherland(target.start, target.end, self.clip)
            elif self.clipAlgorithm is LineClipAlgorithm.LiangBarsky:
                cliped = _clipLiangBarsky(target.start, target.end, self.clip)
            if cliped is None:
                return []
            else:
                p0, p1 = cliped
                target = LineGeometry(p0, p1, target.algorithm)

        # line clip special end

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
