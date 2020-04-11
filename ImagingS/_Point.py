from __future__ import annotations

from math import fabs
from typing import Iterable, Optional, Tuple, Union

import numpy as np

from ImagingS.serialization import PropertySerializable


def feq(a: float, b: float) -> bool:
    return fabs(a-b) < 1e-8


def fsign(a: float) -> int:
    if feq(a, 0):
        return 0
    return 1 if a > 0 else -1


class Point(PropertySerializable):
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        super().__init__()
        self.x = x
        self.y = y

    def __eq__(self, other: Point) -> bool:
        return feq(self.x, other.x) and feq(self.y, other.y)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __neg__(self) -> Point:
        return Point(-self.x, -self.y)

    def __pos__(self) -> Point:
        return self.clone()

    def __mul__(self, other: float) -> Point:
        return Point(self.x * other, self.y * other)

    def __rmul__(self, other: float) -> Point:
        return self * other

    def __abs__(self) -> float:
        return (self.x**2 + self.y**2)**0.5

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def clone(self) -> Point:
        return Point(self.x, self.y)

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = float(value)

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = float(value)

    def toHomogeneous(self) -> np.ndarray:
        return np.array([[self.x], [self.y], [1]])

    def asTuple(self) -> Tuple[float, float]:
        return self.x, self.y

    @staticmethod
    def fromHomogeneous(arr: np.ndarray) -> Point:
        assert arr.shape == (3, 1)
        w = float(arr[2][0])
        assert w != 0
        return Point(float(arr[0][0]) / w, float(arr[1][0]) / w)


class Size(PropertySerializable):
    def __init__(self, width: float = 0.0, height: float = 0.0) -> None:
        super().__init__()
        self.width = width
        self.height = height

    def __eq__(self, obj: Size) -> bool:
        return self.width == obj.width and self.height == obj.height

    def __repr__(self) -> str:
        return f"Size({self.width}, {self.height})"

    def asTuple(self) -> Tuple[float, float]:
        return self.width, self.height

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        self._width = float(value)

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        self._height = float(value)


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
