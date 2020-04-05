from ImagingS.core import Color, Rect, Point
from abc import ABC, abstractmethod
from ImagingS.core.serialization import PropertySerializable
from ImagingS.core.transform import Transform
from typing import List, Optional
from ImagingS.core import IdObject
from ImagingS.core.geometry import Geometry
from . import DrawingContext, BoundingAreaMeasurer, ProxyDrawingContext


class Drawing(PropertySerializable, IdObject, ABC):
    def __init__(self) -> None:
        super().__init__()

    @property
    def clip(self) -> Geometry:
        return self._clip

    @clip.setter
    def clip(self, value: Geometry) -> None:
        self._clip = value

    @abstractmethod
    def render(self, context: DrawingContext) -> None:
        pass

    @property
    def boundingArea(self) -> Rect:
        if not hasattr(self, "_boundingArea"):
            self._boundingArea = None
            measurer = BoundingAreaMeasurer()
            self.render(measurer)
            self._boundingArea = measurer.end_measure()
        elif self._boundingArea is None:  # boundingArea is calculating
            return Rect()
        return self._boundingArea

    def refresh_boundingArea(self) -> None:
        if hasattr(self, "_boundingArea"):
            del self._boundingArea


class DrawingGroup(Drawing):
    def __init__(self):
        super().__init__()
        self.children = []
        self.transform = None

    @property
    def children(self) -> List[Drawing]:
        return self._children

    @children.setter
    def children(self, value: List[Drawing]) -> None:
        self._children = value

    @property
    def transform(self) -> Optional[Transform]:
        return self._transform

    @transform.setter
    def transform(self, value: Optional[Transform]) -> None:
        self._transform = value

    def render(self, context: DrawingContext) -> None:
        def fpoint(position: Point, color: Color):
            if self.transform is not None:
                position = self.transform.transform(position)
            context.point(position, color)

        def farea():
            return context.area

        proxy = ProxyDrawingContext(fpoint, farea)

        for item in self.children:
            item.render(proxy)
