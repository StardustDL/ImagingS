from typing import Optional, List
from ImagingS.core import Point
from abc import ABC, abstractmethod
from ImagingS.core.serialization import PropertySerializable


class Transform(PropertySerializable, ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def transform(self, origin: Point) -> Optional[Point]:
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

    def transform(self, origin: Point) -> Optional[Point]:
        result: Optional[Point] = origin
        for tr in self.children:
            result = tr.transform(result)
            if result is None:
                return None
        return result
