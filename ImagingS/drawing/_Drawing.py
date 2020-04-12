from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from ImagingS import Color, IdObject, IdObjectList, Point, Rect, RectMeasurer
from ImagingS.geometry import Geometry
from ImagingS.serialization import PropertySerializable
from ImagingS.transform import Transform

from . import RenderContext, ProxyRenderContext


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
    def render(self, context: RenderContext) -> None: pass

    @property
    @abstractmethod
    def bounds(self) -> Rect: pass


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
        self.refreshBounds()

    @property
    def transform(self) -> Optional[Transform]:
        return self._transform

    @transform.setter
    def transform(self, value: Optional[Transform]) -> None:
        assert isinstance(value, (type(None), Transform))
        self._transform = value
        self.refreshBounds()

    def render(self, context: RenderContext) -> None:
        renderContext = context
        if self.transform is not None:
            def fpoint(position: Point, color: Color) -> None:
                position = self.transform.transform(position)
                context.point(position, color)

            def fbounds() -> Rect:
                return context.bounds()

            renderContext = ProxyRenderContext(fpoint, fbounds)

        for item in self.children:
            item.render(renderContext)

    @property
    def bounds(self) -> Rect:
        if not hasattr(self, "_bounds"):
            if hasattr(self, "_measurering"):
                return Rect()
            self._measurering = True
            self._bounds = self._calculateBounds()
            del self._measurering
        return self._bounds

    def _calculateBounds(self) -> Rect:
        measurer = RectMeasurer()

        def fpoint(position: Point, color: Color) -> None:
            measurer.append(position)

        def frect() -> Rect:
            return Rect.infinite()

        context = ProxyRenderContext(fpoint, frect)

        self.render(context)
        return measurer.result()

    def refreshBounds(self) -> None:
        if hasattr(self, "_bounds"):
            del self._bounds
