from __future__ import annotations

from typing import Iterable, Optional, Union

from ImagingS.serialization import PropertySerializable
from ImagingS import Point, Size


class Rect(PropertySerializable):
    _infinite: Optional[Rect] = None

    def __init__(self, origin: Optional[Point] = None, size: Optional[Size] = None) -> None:
        super().__init__()
        self.origin = origin if origin else Point()
        self.size = size if size else Size()

    @classmethod
    def infinite(cls) -> Rect:
        if cls._infinite is None:
            cls._infinite = Rect.fromPoints(Point(
                float("-inf"), float("-inf")), Point(float("inf"), float("inf")))
        return cls._infinite

    @staticmethod
    def fromPoints(p1: Point, p2: Point) -> Rect:
        x1, y1 = p1.asTuple()
        x2, y2 = p2.asTuple()
        xmin, xmax = min(x1, x2), max(x1, x2)
        ymin, ymax = min(y1, y2), max(y1, y2)
        return Rect(Point(xmin, ymin), Size(xmax - xmin, ymax - ymin))

    def __eq__(self, obj: Rect) -> bool:
        return self.origin == obj.origin and self.size == obj.size

    def __repr__(self) -> str:
        return f"Rect({self.origin}, {self.size})"

    def __contains__(self, point: Point) -> bool:
        delta = point - self.origin
        return 0 <= delta.x <= self.size.width and 0 <= delta.y <= self.size.height

    @property
    def origin(self) -> Point:
        return self._origin

    @origin.setter
    def origin(self, value: Point) -> None:
        assert isinstance(value, Point)
        self._origin = value

    @property
    def size(self) -> Size:
        return self._size

    @size.setter
    def size(self, value: Size) -> None:
        assert isinstance(value, Size)
        self._size = value

    def vertex(self) -> Point:
        return Point(self.origin.x+self.size.width, self.origin.y+self.size.height)


class RectMeasurer:
    def __init__(self) -> None:
        super().__init__()
        self._lx = float("inf")
        self._ly = float("inf")
        self._rx = float("-inf")
        self._ry = float("-inf")

    def result(self) -> Rect:
        result = Rect.fromPoints(Point(
            self._lx, self._ly), Point(self._rx, self._ry))
        return result

    def append(self, position: Union[Point, Iterable[Point]]) -> None:
        if isinstance(position, Point):
            x, y = position.asTuple()
            self._lx = min(self._lx, x)
            self._ly = min(self._ly, y)
            self._rx = max(self._rx, x)
            self._ry = max(self._ry, y)
        else:
            for p in position:
                self.append(p)
