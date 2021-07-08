from abc import ABC, abstractmethod

from ImagingS import IdObject, IdObjectList, Point
from ImagingS.serialization import PropertySerializable


class Transform(PropertySerializable, IdObject, ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def transform(self, origin: Point) -> Point: pass


class TransformGroup(Transform):
    def __init__(self) -> None:
        super().__init__()
        self.children = IdObjectList()

    @property
    def children(self) -> IdObjectList[Transform]:
        return self._children

    @children.setter
    def children(self, value: IdObjectList[Transform]) -> None:
        assert isinstance(value, IdObjectList)
        self._children = value

    def transform(self, origin: Point) -> Point:
        result = origin
        for tr in self.children:
            result = tr.transform(result)
        return result
