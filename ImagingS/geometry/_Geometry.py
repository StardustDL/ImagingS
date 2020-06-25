from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, List, Optional

from ImagingS import Point, Rect, RectMeasurer
from ImagingS.drawing import Pen
from ImagingS.serialization import PropertySerializable
from ImagingS.transform import Transform


class Geometry(PropertySerializable, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.transform = None

    @property
    def transform(self) -> Optional[Transform]:
        return self._transform

    @transform.setter
    def transform(self, value: Optional[Transform]) -> None:
        assert isinstance(value, (type(None), Transform))
        self._transform = value
        self.refreshBounds()

    @abstractmethod
    def strokePoints(self, pen: Pen) -> Iterable[Point]: pass

    @abstractmethod
    def fillPoints(self) -> Iterable[Point]: pass

    def inStroke(self, pen: Pen, point: Point) -> bool:
        return point in self.strokePoints(pen)

    def inFill(self, point: Point) -> bool:
        return point in self.fillPoints()

    @abstractmethod
    def transformed(self) -> Geometry: pass

    @property
    def bounds(self) -> Rect:
        if not hasattr(self, "_bounds"):
            if hasattr(self, "_measurering"):
                return Rect()
            self._measurering = True
            self._bounds = self._calculateBounds()
            del self._measurering
        return self._bounds

    def _calculateBounds(self) -> Rect:
        measurer = RectMeasurer()
        for p in self.strokePoints(Pen()):
            measurer.append(p)
        return measurer.result()

    def refreshBounds(self) -> None:
        if hasattr(self, "_bounds"):
            del self._bounds


class GeometryGroup(Geometry):
    def __init__(self):
        super().__init__()
        self.children = []

    @property
    def children(self) -> List[Geometry]:
        return self._children

    @children.setter
    def children(self, value: List[Geometry]) -> None:
        assert isinstance(value, list)
        self._children = value

    def transformed(self) -> Geometry:
        if self.transform is None:
            return self
        else:
            result = GeometryGroup()
            for c in self.children:
                result.children.append(c.transformed())
            return result

    def strokePoints(self, pen: Pen) -> Iterable[Point]:
        for child in self.children:
            for point in child.strokePoints(pen):
                if self.transform is None:
                    yield point
                else:
                    yield self.transform.transform(point)

    def fillPoints(self) -> Iterable[Point]:
        for child in self.children:
            for point in child.fillPoints():
                if self.transform is None:
                    yield point
                else:
                    yield self.transform.transform(point)

    def inStroke(self, pen: Pen, point: Point) -> bool:
        for child in self.children:
            if child.inStroke(pen, point):
                return True
        return False

    def inFill(self, point: Point) -> bool:
        for child in self.children:
            if child.inFill(point):
                return True
        return False
