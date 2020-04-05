from ImagingS.core.drawing import Pen
from ImagingS.core import Point
from abc import ABC, abstractmethod
from typing import Iterable, List
from ImagingS.core.serialization import PropertySerializable
from ImagingS.core.transform import Transform


class Geometry(PropertySerializable, ABC):
    @property
    def transform(self) -> Transform:
        return self._transform

    @transform.setter
    def transform(self, value: Transform) -> None:
        self._transform = value

    @abstractmethod
    def stroke(self, pen: Pen) -> Iterable[Point]:
        pass

    @abstractmethod
    def fill(self) -> Iterable[Point]:
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

    def stroke(self, pen: Pen) -> Iterable[Point]:
        for child in self.children:
            for point in child.stroke(pen):
                if self.transform is None:
                    yield point
                else:
                    yield self.transform.transform(point)

    def fill(self) -> Iterable[Point]:
        for child in self.children:
            for point in child.fill():
                if self.transform is None:
                    yield point
                else:
                    yield self.transform.transform(point)
