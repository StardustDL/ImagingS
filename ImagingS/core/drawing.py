from ImagingS.core import Color, Point, RectArea, Size
from abc import ABC, abstractmethod
from ImagingS.core.serialization import Serializable
from ImagingS.core.transform import Transform
from typing import List
from ImagingS.core import IdObject


class DrawingContext(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def point(self, position: Point, color: Color) -> None:
        pass

    @property
    @abstractmethod
    def size(self) -> Size:
        pass


class Drawing(Serializable, IdObject, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.transforms: List[Transform] = []

    @abstractmethod
    def render(self, context: DrawingContext) -> None:
        pass

    @abstractmethod
    def boundingArea(self, context: DrawingContext) -> RectArea:
        pass


class DrawingGroup(Drawing):
    def __init__(self):
        super().__init__()
        self.children: List[Drawing] = []
