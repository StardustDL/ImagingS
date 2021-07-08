from abc import ABC, abstractmethod
from typing import Callable, Iterable

import numpy as np

from ImagingS import Color, Point, Rect, Size
from ImagingS.brush import Brush


class RenderContext(ABC):
    @abstractmethod
    def _point(self, position: Point, color: Color) -> None: pass

    @abstractmethod
    def bounds(self) -> Rect: pass

    def point(self, position: Point, color: Color) -> None:
        if position in self.bounds():
            self._point(position, color)

    def points(self, positions: Iterable[Point], brush: Brush) -> None:
        bounds = self.bounds()
        for p in positions:
            self.point(p, brush.colorAt(p, bounds))


class NumpyArrayRenderContext(RenderContext):
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
        self._bounds = Rect(
            Point(), Size(value.shape[1], value.shape[0]))

    def _point(self, position: Point, color: Color) -> None:
        x, y = map(int, position.asTuple())
        self.array[y, x, 0] = color.r
        self.array[y, x, 1] = color.g
        self.array[y, x, 2] = color.b

    def bounds(self) -> Rect:
        return self._bounds


class ProxyRenderContext(RenderContext):
    def __init__(self, fpoint: Callable[[Point, Color], None], fbounds: Callable[[], Rect]) -> None:
        super().__init__()
        self._fpoint = fpoint
        self._fbounds = fbounds

    def _point(self, position: Point, color: Color) -> None:
        self._fpoint(position, color)

    def bounds(self) -> Rect:
        return self._fbounds()


class ClipRenderContext(ProxyRenderContext):
    def __init__(self, bounds: Rect, innerContext: RenderContext) -> None:
        super().__init__(innerContext.point, lambda: bounds)
