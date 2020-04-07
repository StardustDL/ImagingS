from __future__ import annotations

from math import fabs
from typing import Optional, Tuple

import numpy as np

from ImagingS.serialization import PropertySerializable


class Point(PropertySerializable):
    def __init__(self) -> None:
        super().__init__()
        self.x = 0
        self.y = 0

    @staticmethod
    def create(x: float, y: float) -> Point:
        result = Point()
        result.x = x
        result.y = y
        return result

    def __eq__(self, other: Point) -> bool:
        return fabs(self.x - other.x) < 1e-8 and fabs(self.y - other.y) < 1e-8

    def __add__(self, other: Point) -> Point:
        return Point.create(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point.create(self.x - other.x, self.y - other.y)

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = value

    def to_array(self) -> np.ndarray:
        return np.array([[self.x], [self.y]])

    def as_tuple(self) -> Tuple[float, float]:
        return self.x, self.y

    @staticmethod
    def from_array(arr: np.ndarray) -> Point:
        assert len(arr) == 2 and len(arr[0]) == 1 and len(arr[1]) == 1
        return Point.create(float(arr[0][0]), float(arr[1][0]))


class Size(PropertySerializable):
    def __init__(self) -> None:
        super().__init__()
        self.width = 0
        self.height = 0

    @staticmethod
    def create(width: float, height: float) -> Size:
        result = Size()
        result.width = width
        result.height = height
        return result

    def __eq__(self, obj) -> bool:
        if isinstance(obj, Size):
            return self.width == obj.width and self.height == obj.height
        return False

    def __repr__(self) -> str:
        return f"Size({self.width}, {self.height})"

    def as_tuple(self) -> Tuple[float, float]:
        return self.width, self.height

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        self._width = value

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        self._height = value


class Rect(PropertySerializable):
    _infinite: Optional[Rect] = None

    def __init__(self) -> None:
        super().__init__()
        self.origin = Point()
        self.size = Size()

    @staticmethod
    def create(origin: Point, size: Size) -> Rect:
        result = Rect()
        result.origin = origin
        result.size = size
        return result

    @classmethod
    def infinite(cls) -> Rect:
        if cls._infinite is None:
            cls._infinite = Rect.from_points(Point.create(
                float("-inf"), float("-inf")), Point.create(float("inf"), float("inf")))
        return cls._infinite

    @staticmethod
    def from_points(p1: Point, p2: Point) -> Rect:
        x1, y1 = p1.as_tuple()
        x2, y2 = p2.as_tuple()
        xmin, xmax = min(x1, x2), max(x1, x2)
        ymin, ymax = min(y1, y2), max(y1, y2)
        return Rect.create(Point.create(xmin, ymin), Size.create(xmax - xmin, ymax - ymin))

    def __eq__(self, obj) -> bool:
        if isinstance(obj, Rect):
            return self.origin == obj.origin and self.size == obj.size
        return False

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
        self._origin = value

    @property
    def size(self) -> Size:
        return self._size

    @size.setter
    def size(self, value: Size) -> None:
        self._size = value
