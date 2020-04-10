from __future__ import annotations

from typing import Optional

from ImagingS.brush import Brush, Brushes
from ImagingS.geometry import Geometry

from . import Drawing, DrawingContext, Pen


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
        self.refreshBoundingRect()

    def render(self, context: DrawingContext) -> None:
        if self.geometry is None:
            return
        rect = context.rect()
        for point in self.geometry.strokePoints(self.stroke):
            if point in rect:
                context.point(point,
                              self.stroke.brush.colorAt(point, self.boundingRect))
        for point in self.geometry.fillPoints():
            if point in rect:
                context.point(point, self.fill.colorAt(
                    point, self.boundingRect))
