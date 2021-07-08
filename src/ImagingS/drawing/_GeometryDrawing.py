from __future__ import annotations

from typing import Optional

from ImagingS import Rect
from ImagingS.brush import Brush, Brushes
from ImagingS.geometry import Geometry

from . import Drawing, Pen, RenderContext


class GeometryDrawing(Drawing):
    def __init__(self, geometry: Optional[Geometry] = None) -> None:
        super().__init__()
        self.geometry = geometry
        self.stroke = Pen()
        self.fill = Brushes.White

    @property
    def stroke(self) -> Pen:
        return self._stroke

    @stroke.setter
    def stroke(self, value: Pen) -> None:
        assert isinstance(value, Pen)
        self._stroke = value

    @property
    def fill(self) -> Brush:
        return self._fill

    @fill.setter
    def fill(self, value: Brush) -> None:
        assert isinstance(value, Brush)
        self._fill = value

    @property
    def geometry(self) -> Optional[Geometry]:
        return self._geometry

    @geometry.setter
    def geometry(self, value: Optional[Geometry]) -> None:
        assert isinstance(value, (type(None), Geometry))
        self._geometry = value

    def render(self, context: RenderContext) -> None:
        if self.geometry is None:
            return
        context.points(self.geometry.fillPoints(), self.fill)
        context.points(self.geometry.strokePoints(self.stroke), self.stroke.brush)

    @property
    def bounds(self) -> Rect:
        if self.geometry is None:
            return Rect()
        else:
            return self.geometry.bounds
