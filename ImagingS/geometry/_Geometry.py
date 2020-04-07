from abc import ABC, abstractmethod
from typing import Iterable, List, Optional

from ImagingS import Point
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
        self._transform = value

    @abstractmethod
    def stroke_points(self, pen: Pen) -> Iterable[Point]:
        pass

    @abstractmethod
    def fill_points(self) -> Iterable[Point]:
        pass

    def in_stroke(self, pen: Pen, point: Point) -> bool:
        return point in self.stroke_points(pen)

    def in_fill(self, point: Point) -> bool:
        return point in self.fill_points


class GeometryGroup(Geometry):
    def __init__(self):
        super().__init__()
        self.children = []

    @property
    def children(self) -> List[Geometry]:
        return self._children

    @children.setter
    def children(self, value: List[Geometry]) -> None:
        self._children = value

    def stroke_points(self, pen: Pen) -> Iterable[Point]:
        for child in self.children:
            for point in child.stroke_points(pen):
                if self.transform is None:
                    yield point
                else:
                    yield self.transform.transform(point)

    def fill_points(self) -> Iterable[Point]:
        for child in self.children:
            for point in child.fill_points():
                if self.transform is None:
                    yield point
                else:
                    yield self.transform.transform(point)

    def in_stroke(self, pen: Pen, point: Point) -> bool:
        for child in self.children:
            if child.in_stroke(pen, point):
                return True
        return False

    def in_fill(self, point: Point) -> bool:
        for child in self.children:
            if child.in_fill(point):
                return True
        return False
