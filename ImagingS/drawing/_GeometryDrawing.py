from __future__ import annotations

from ImagingS.brush import Brush, Brushes
from ImagingS.geometry import Geometry

from . import Drawing, DrawingContext, Pen


class GeometryDrawing(Drawing):
    def __init__(self) -> None:
        super().__init__()
        self.stroke = Pen()
        self.fill = Brushes.White

    @staticmethod
    def create(geometry: Geometry) -> GeometryDrawing:
        result = GeometryDrawing()
        result.geometry = geometry
        return result

    @property
    def stroke(self) -> Pen:
        return self._stroke

    @stroke.setter
    def stroke(self, value: Pen) -> None:
        self._stroke = value

    @property
    def fill(self) -> Brush:
        return self._fill

    @fill.setter
    def fill(self, value: Brush) -> None:
        self._fill = value

    @property
    def geometry(self) -> Geometry:
        return self._geometry

    @geometry.setter
    def geometry(self, value: Geometry) -> None:
        self._geometry = value
        self.refreshBoundingRect()

    def render(self, context: DrawingContext) -> None:
        rect = context.rect()
        for point in self.geometry.strokePoints(self.stroke):
            if point in rect:
                context.point(point,
                              self.stroke.brush.colorAt(point, self.boundingRect))
        for point in self.geometry.fillPoints():
            if point in rect:
                context.point(point, self.fill.colorAt(
                    point, self.boundingRect))
