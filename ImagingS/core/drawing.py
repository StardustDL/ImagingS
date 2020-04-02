from ImagingS.core import Color, Point, RectArea, Size
from abc import ABC, abstractmethod
from ImagingS.core.serialization import PropertySerializable
from ImagingS.core.transform import Transform
from typing import List, Optional
from ImagingS.core import IdObject


class DrawingContext(ABC):
    @abstractmethod
    def point(self, position: Point, color: Color) -> None:
        pass

    @property
    @abstractmethod
    def size(self) -> Size:
        pass


class Drawing(PropertySerializable, IdObject, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.transform = None

    @property
    def transform(self) -> Optional[Transform]:
        return self._transform

    @transform.setter
    def transform(self, value: Optional[Transform]) -> None:
        self._transform = value

    @abstractmethod
    def render(self, context: DrawingContext) -> None:
        pass

    @property
    @abstractmethod
    def boundingArea(self) -> RectArea:
        pass


class DrawingGroup(Drawing):
    def __init__(self):
        super().__init__()
        self.children = []

    @property
    def children(self) -> List[Drawing]:
        return self._children

    @children.setter
    def children(self, value: List[Drawing]) -> None:
        self._children = value

    def render(self, context: DrawingContext) -> None:
        for item in self.children:
            item.render(context)

    @property
    def boundingArea(self) -> RectArea:
        if len(self.children) == 0:
            return RectArea()
        return self.children[0].boundingArea
