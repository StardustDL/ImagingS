from typing import Optional, List
from ImagingS.core import IdObject, Point
from abc import ABC, abstractmethod


class Transform(IdObject, ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def transform(self, origin: Point) -> Optional[Point]:
        pass


class TransformGroup(Transform):
    def __init__(self):
        super().__init__()
        self.children: List[Transform] = []
