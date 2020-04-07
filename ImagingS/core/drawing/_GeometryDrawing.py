from __future__ import annotations

from ImagingS.core.brush import Brush, Brushes
from ImagingS.core.geometry import Geometry

from . import Drawing, DrawingContext, Pen


class GeometryDrawing(Drawing):
    def __init__(self) -> None:
        super().__init__()
        self.stroke = Pen()
        self.fill = Brushes.White()

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
        self.refresh_boundingArea()

    def render(self, context: DrawingContext) -> None:
        area = context.area()
        for point in self.geometry.stroke_points(self.stroke):
            if point in area:
                context.point(point,
                              self.stroke.brush.color_at(point, self.boundingArea))
        for point in self.geometry.fill_points():
            if point in area:
                context.point(point, self.fill.color_at(
                    point, self.boundingArea))
