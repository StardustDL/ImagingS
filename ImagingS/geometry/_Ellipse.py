from __future__ import annotations

from typing import Iterable, Tuple, Iterator

from ImagingS import Point, Rect
from ImagingS.drawing import Pen

from . import Geometry


def _gen(center: Point, radius: Tuple[float, float]) -> Iterator[Point]:
    def gen_first(a: int, b: int) -> Iterator[Point]:
        x, y = 0, b
        a2, b2 = a**2, b**2
        d = b2 - a2*(b-0.25)
        yield Point.create(x, y)
        sp = a2 / (a2+b2)**0.5
        while x < sp:
            if d < 0:
                d += b2*(2*x+3)
            else:
                d += b2*(2*x+3)+a2*(-2*y+2)
                y -= 1
            x += 1
            yield Point.create(x, y)
        d = b2*(x+0.5)**2 + a2*(y-1)**2 - a2*b2
        while y >= 0:
            if d < 0:
                d += b2*(2*x+2) + a2*(-2*y+3)
                x += 1
            else:
                d += a2*(-2*y+3)
            y -= 1
            yield Point.create(x, y)
    for p in gen_first(round(radius[0]), round(radius[1])):
        yield center + p
        yield center - p
        yield center + Point.create(p.x, -p.y)
        yield center + Point.create(-p.x, p.y)


class EllipseGeometry(Geometry):
    def __init__(self) -> None:
        super().__init__()
        self.center = Point()
        self.radius = (1, 1)

    @staticmethod
    def create(center: Point, radius: Tuple[float, float]) -> EllipseGeometry:
        result = EllipseGeometry()
        result.center = center
        result.radius = radius
        return result

    @staticmethod
    def from_rect(rect: Rect) -> EllipseGeometry:
        po, pv = rect.origin, rect.vertex()
        result = EllipseGeometry()
        result.center = (po+pv)*0.5
        result.radius = (rect.size.width/2, rect.size.height/2)
        return result

    @property
    def center(self) -> Point:
        return self._center

    @center.setter
    def center(self, value: Point) -> None:
        self._center = value

    @property
    def radius(self) -> Tuple[float, float]:
        return self._radius

    @radius.setter
    def radius(self, value: Tuple[float, float]) -> None:
        self._radius = value

    def stroke_points(self, pen: Pen) -> Iterable[Point]:
        return _gen(self.center, self.radius)

    def fill_points(self) -> Iterable[Point]:
        return []
