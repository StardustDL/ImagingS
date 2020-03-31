from __future__ import annotations
import numpy as np


class Point(object):
    def __init__(self, x: float, y: float) -> None:
        self._x = x
        self._y = y

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


class Color(object):
    def __init__(self, r: int, g: int, b: int) -> None:
        self._r = r
        self._g = g
        self._b = b

    @property
    def r(self) -> float:
        return self._r

    @property
    def g(self) -> float:
        return self._g

    @property
    def b(self) -> float:
        return self._b


class Size(object):
    def __init__(self, width: float, height: float) -> None:
        self._width = width
        self._height = height

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height


class RectArea(object):
    def __init__(self, origin: Point, size: Size) -> None:
        self._origin = origin
        self._size = size

    @property
    def origin(self) -> Point:
        return self._origin

    @property
    def size(self) -> Size:
        return self._size
