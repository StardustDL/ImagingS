from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from ImagingS import Color, IdObject, IdObjectList, Point, Rect
from ImagingS.geometry import Geometry
from ImagingS.serialization import PropertySerializable
from ImagingS.transform import Transform

from . import BoundingRectMeasurer, DrawingContext, ProxyDrawingContext


class Drawing(PropertySerializable, IdObject, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.clip = None
        self.setParent(None)

    @property
    def clip(self) -> Optional[Geometry]:
        return self._clip

    @clip.setter
    def clip(self, value: Optional[Geometry]) -> None:
        assert isinstance(value, (type(None), Geometry))
        self._clip = value

    @abstractmethod
    def render(self, context: DrawingContext) -> None: pass

    @property
    def boundingRect(self) -> Rect:
        if not hasattr(self, "_boundingRect"):
            if hasattr(self, "_measurering"):
                return Rect()
            self._boundingRect = self._calculateBoundingRect()
        return self._boundingRect

    def _calculateBoundingRect(self) -> Rect:
        self._measurering = True
        measurer = BoundingRectMeasurer()
        self.render(measurer)
        del self._measurering
        return measurer.endMeasure()

    def refreshBoundingRect(self) -> None:
        if hasattr(self, "_boundingRect"):
            del self._boundingRect


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
        assert isinstance(value, IdObjectList)
        self._children = value

    @property
    def transform(self) -> Optional[Transform]:
        return self._transform

    @transform.setter
    def transform(self, value: Optional[Transform]) -> None:
        assert isinstance(value, (type(None), Transform))
        self._transform = value

    def render(self, context: DrawingContext) -> None:
        renderContext = context
        if self.transform is not None:
            def fpoint(position: Point, color: Color) -> None:
                position = self.transform.transform(position)
                context.point(position, color)

            def frect() -> Rect:
                return context.rect()

            renderContext = ProxyDrawingContext(fpoint, frect)

        for item in self.children:
            item.render(renderContext)
