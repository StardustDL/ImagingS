from ImagingS.core import Color, Point, RectArea, Size
from abc import ABC, abstractmethod
from ImagingS.core.serialization import PropertySerializable
from ImagingS.core.transform import Transform
from typing import List, Optional
from ImagingS.core import IdObject
import numpy as np


class DrawingContext(ABC):
    @abstractmethod
    def point(self, position: Point, color: Color) -> None:
        pass

    @abstractmethod
    def area(self) -> RectArea:
        pass


class BoundingAreaMeasurer(DrawingContext):
    def __init__(self):
        self._lx = float("inf")
        self._ly = float("inf")
        self._rx = float("-inf")
        self._ry = float("-inf")

    def end_measure(self) -> RectArea:
        result = RectArea.from_points(Point.create(
            self._lx, self._ly), Point.create(self._rx, self._ry))
        return result

    def point(self, position: Point, color: Color) -> None:
        x, y = position.as_tuple()
        self._lx = min(self._lx, x)
        self._ly = min(self._ly, y)
        self._rx = max(self._rx, x)
        self._ry = max(self._ry, y)

    def area(self) -> RectArea:
        return RectArea.infinite()


class NumpyArrayDrawingContext(DrawingContext):
    @staticmethod
    def create_array(size: Size) -> np.ndarray:
        result = np.zeros([size.height, size.width, 3], np.uint8)
        result.fill(255)
        return result

    def __init__(self, array: np.ndarray):
        self.array = array

    @property
    def array(self) -> np.ndarray:
        return self._array

    @array.setter
    def array(self, value: np.ndarray) -> None:
        assert value.dtype == np.uint8
        assert len(value.shape) == 3
        assert value.shape[2] == 3
        self._array = value
        self._area = RectArea.create(
            Point(), Size.create(value.shape[1], value.shape[0]))

    def point(self, position: Point, color: Color) -> None:
        x, y = map(int, position.as_tuple())
        self.array[y, x, 0] = color.r
        self.array[y, x, 1] = color.g
        self.array[y, x, 2] = color.b

    def area(self) -> RectArea:
        return self._area


class Drawing(PropertySerializable, IdObject, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.transform = None

    @property
    def transform(self) -> Optional[Transform]:
        return self._transform

    @transform.setter
    def transform(self, value: Optional[Transform]) -> None:
        self._transform = value
        self.refresh_boundingArea()

    @abstractmethod
    def render(self, context: DrawingContext) -> None:
        pass

    @property
    def boundingArea(self) -> RectArea:
        if not hasattr(self, "_boundingArea"):
            self._boundingArea = None
            measurer = BoundingAreaMeasurer()
            self.render(measurer)
            self._boundingArea = measurer.end_measure()
        elif self._boundingArea is None:  # boundingArea is calculating
            return RectArea()
        return self._boundingArea

    def refresh_boundingArea(self) -> None:
        if hasattr(self, "_boundingArea"):
            del self._boundingArea


class DrawingGroup(Drawing):
    def __init__(self):
        super().__init__()
        self.children = []

    @property
    def children(self) -> List[Drawing]:
        return self._children

    @children.setter
    def children(self, value: List[Drawing]) -> None:
        self._children = value

    def render(self, context: DrawingContext) -> None:
        for item in self.children:
            item.render(context)
