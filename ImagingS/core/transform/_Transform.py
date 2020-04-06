from abc import ABC, abstractmethod
from typing import List

from ImagingS.core import Point
from ImagingS.core.serialization import PropertySerializable


class Transform(PropertySerializable, ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def transform(self, origin: Point) -> Point:
        pass


class TransformGroup(Transform):
    def __init__(self):
        super().__init__()
        self.children = []

    @property
    def children(self) -> List[Transform]:
        return self._children

    @children.setter
    def children(self, value: List[Transform]) -> None:
        self._children = value

    def transform(self, origin: Point) -> Point:
        result = origin
        for tr in self.children:
            result = tr.transform(result)
        return result
