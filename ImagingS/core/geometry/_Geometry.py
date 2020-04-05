from ImagingS.core.drawing import Pen
from ImagingS.core import Point
from abc import ABC, abstractmethod
from typing import Iterable, List, Optional
from ImagingS.core.serialization import PropertySerializable
from ImagingS.core.transform import Transform


class Geometry(PropertySerializable, ABC):
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

    @abstractmethod
    def in_stroke(self, pen: Pen, point: Point) -> bool:
        pass

    @abstractmethod
    def in_fill(self, point: Point) -> bool:
        pass


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
