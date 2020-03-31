from ImagingS.core import Color, Point, RectArea, Size
from abc import ABC, abstractmethod
from ImagingS.core.transform import Transform
from typing import List, Optional


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


class Drawing(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.transform: Optional[Transform] = None
        self.id: str = ""

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
