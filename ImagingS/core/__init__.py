from __future__ import annotations
from ImagingS.core.serialization import Serializable
from typing import Dict, Any
from math import fabs
import numpy as np


class Point(Serializable):
    def __init__(self, x: float, y: float) -> None:
        self._x = x
        self._y = y

    def __eq__(self, other: Point) -> bool:
        return fabs(self._x - other._x) < 1e-8 and fabs(self._y - other._y) < 1e-8

    def __add__(self, other: Point) -> Point:
        return Point(self._x + other._x, self._y + other._y)

    def __sub__(self, other: Point) -> Point:
        return Point(self._x - other._x, self._y - other._y)

    def __repr__(self) -> str:
        return f"Point({self._x}, {self._y})"

    @staticmethod
    def deserialize(data: Dict) -> Any:
        return Point(data["_x"], data["_y"])

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def to_array(self) -> np.ndarray:
        return np.array([[self._x], [self._y]])

    @staticmethod
    def from_array(arr: np.ndarray) -> Point:
        assert len(arr) == 2 and len(arr[0]) == 1 and len(arr[1]) == 1
        return Point(arr[0][0], arr[1][0])


class Color(Serializable):
    def __init__(self, r: int, g: int, b: int) -> None:
        self._r = r
        self._g = g
        self._b = b

    def __eq__(self, obj) -> bool:
        if isinstance(obj, Color):
            return self._r == obj._r and self._g == obj._g and self._b == obj._b
        return False

    def __repr__(self) -> str:
        return f"Color({self._r}, {self._g}, {self._b})"

    @staticmethod
    def deserialize(data: Dict) -> Any:
        return Color(data["_r"], data["_g"], data["_b"])

    @property
    def r(self) -> float:
        return self._r

    @property
    def g(self) -> float:
        return self._g

    @property
    def b(self) -> float:
        return self._b


class Size(Serializable):
    def __init__(self, width: float, height: float) -> None:
        self._width = width
        self._height = height

    def __eq__(self, obj) -> bool:
        if isinstance(obj, Size):
            return self._width == obj._width and self._height == obj._height
        return False

    def __repr__(self) -> str:
        return f"Size({self._width}, {self._height})"

    @staticmethod
    def deserialize(data: Dict) -> Any:
        return Size(data["_width"], data["_height"])

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height


class RectArea(Serializable):
    def __init__(self, origin: Point, size: Size) -> None:
        self._origin = origin
        self._size = size

    def __eq__(self, obj) -> bool:
        if isinstance(obj, RectArea):
            return self._origin == obj._origin and self._size == obj._size
        return False

    @staticmethod
    def deserialize(data: Dict) -> Any:
        return RectArea(data["_origin"], data["_size"])

    @property
    def origin(self) -> Point:
        return self._origin

    @property
    def size(self) -> Size:
        return self._size
