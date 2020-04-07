from abc import ABC, abstractmethod
from typing import Optional

from ImagingS import Color, IdObject, IdObjectList, Point, Rect
from ImagingS.geometry import Geometry
from ImagingS.serialization import PropertySerializable
from ImagingS.transform import Transform

from . import BoundingAreaMeasurer, DrawingContext, ProxyDrawingContext


class Drawing(PropertySerializable, IdObject, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.clip = None

    @property
    def clip(self) -> Optional[Geometry]:
        return self._clip

    @clip.setter
    def clip(self, value: Optional[Geometry]) -> None:
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
    def __init__(self) -> None:
        super().__init__()
        self.children = IdObjectList()
        self.transform = None

    @property
    def children(self) -> IdObjectList[Drawing]:
        return self._children

    @children.setter
    def children(self, value: IdObjectList[Drawing]) -> None:
        self._children = value

    @property
    def transform(self) -> Optional[Transform]:
        return self._transform

    @transform.setter
    def transform(self, value: Optional[Transform]) -> None:
        self._transform = value

    def render(self, context: DrawingContext) -> None:
        renderContext = context
        if self.transform is not None:
            def fpoint(position: Point, color: Color) -> None:
                position = self.transform.transform(position)
                context.point(position, color)

            def farea() -> Rect:
                return context.area()

            renderContext = ProxyDrawingContext(fpoint, farea)

        for item in self.children:
            item.render(renderContext)
