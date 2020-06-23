from __future__ import annotations

from typing import Optional, Tuple

from ImagingS import Point, Rect

from . import LineGeometry, LineClipAlgorithm


def _clipCohenSutherland(start: Point, end: Point, area: Rect) -> Optional[Tuple[Point, Point]]:
    if start == end:
        if start in area:
            return start, end
        else:
            return None
    aori, aver = area.origin, area.vertex()
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
            assert False  # will not full zero, not happend
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
    aori, aver = area.origin, area.vertex()
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


class LineClipper:
    def __init__(self, line: LineGeometry) -> None:
        self.line = line

    def clip(self, area: Rect, algorithm: LineClipAlgorithm) -> Optional[LineGeometry]:
        if area is not None:
            cliped = None
            if algorithm is LineClipAlgorithm.CohenSutherland:
                cliped = _clipCohenSutherland(self.line.start, self.line.end, area)
            elif algorithm is LineClipAlgorithm.LiangBarsky:
                cliped = _clipLiangBarsky(self.line.start, self.line.end, area)
            if cliped is None:
                return None
            else:
                p0, p1 = cliped
                return LineGeometry(p0, p1, self.line.algorithm)
