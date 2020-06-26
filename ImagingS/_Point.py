from __future__ import annotations

from typing import Tuple

import numpy as np

from ImagingS.serialization import PropertySerializable
from ImagingS import feq


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
