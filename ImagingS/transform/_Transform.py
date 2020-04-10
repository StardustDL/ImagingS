from abc import ABC, abstractmethod
from typing import List

from ImagingS import Point
from ImagingS.serialization import PropertySerializable


class Transform(PropertySerializable, ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def transform(self, origin: Point) -> Point: pass


class TransformGroup(Transform):
    def __init__(self) -> None:
        super().__init__()
        self.children = []

    @property
    def children(self) -> List[Transform]:
        return self._children

    @children.setter
    def children(self, value: List[Transform]) -> None:
        assert isinstance(value, list)
        self._children = value

    def transform(self, origin: Point) -> Point:
        result = origin
        for tr in self.children:
            result = tr.transform(result)
        return result
