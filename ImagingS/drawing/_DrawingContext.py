from abc import ABC, abstractmethod
from typing import Callable

import numpy as np

from ImagingS import Color, Point, Rect, Size


class DrawingContext(ABC):
    @abstractmethod
    def point(self, position: Point, color: Color) -> None: pass

    @abstractmethod
    def rect(self) -> Rect: pass


class BoundingRectMeasurer(DrawingContext):
    def __init__(self) -> None:
        super().__init__()
        self._lx = float("inf")
        self._ly = float("inf")
        self._rx = float("-inf")
        self._ry = float("-inf")

    def endMeasure(self) -> Rect:
        result = Rect.fromPoints(Point.create(
            self._lx, self._ly), Point.create(self._rx, self._ry))
        return result

    def point(self, position: Point, color: Color) -> None:
        x, y = position.asTuple()
        self._lx = min(self._lx, x)
        self._ly = min(self._ly, y)
        self._rx = max(self._rx, x)
        self._ry = max(self._ry, y)

    def rect(self) -> Rect:
        return Rect.infinite()


class NumpyArrayDrawingContext(DrawingContext):
    @staticmethod
    def create_array(size: Size) -> np.ndarray:
        result = np.zeros([int(size.height), int(size.width), 3], np.uint8)
        result.fill(255)
        return result

    def __init__(self, array: np.ndarray) -> None:
        self.array = array

    @property
    def array(self) -> np.ndarray:
        super().__init__()
        return self._array

    @array.setter
    def array(self, value: np.ndarray) -> None:
        assert isinstance(value, np.ndarray)
        assert value.dtype == np.uint8
        assert len(value.shape) == 3
        assert value.shape[2] == 3
        self._array = value
        self._rect = Rect.create(
            Point(), Size.create(value.shape[1], value.shape[0]))

    def point(self, position: Point, color: Color) -> None:
        x, y = map(int, position.asTuple())
        self.array[y, x, 0] = color.r
        self.array[y, x, 1] = color.g
        self.array[y, x, 2] = color.b

    def rect(self) -> Rect:
        return self._rect


class ProxyDrawingContext(DrawingContext):
    def __init__(self, fpoint: Callable[[Point, Color], None], frect: Callable[[], Rect]) -> None:
        super().__init__()
        self._fpoint = fpoint
        self._frect = frect

    def point(self, position: Point, color: Color) -> None:
        self._fpoint(position, color)

    def rect(self) -> Rect:
        return self._frect()
