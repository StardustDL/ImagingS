from typing import Optional, List
from ImagingS.core import Point
from abc import ABC, abstractmethod
from ._Clip import Clip
from ._Matrix import Matrix
from ._Rotate import Rotate
from ._Scale import Scale
from ._Skew import Skew
from ._Translate import Translate


class Transform(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def transform(self, origin: Point) -> Optional[Point]:
        pass


class TransformGroup(Transform):
    def __init__(self):
        super().__init__()
        self.children: List[Transform] = []


__all__ = (
    "Transform",
    "Clip",
    "Matrix",
    "Rotate",
    "Scale",
    "Skew",
    "Translate",
)
