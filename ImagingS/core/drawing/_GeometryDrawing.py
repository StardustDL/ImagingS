from . import Drawing, Pen, DrawingContext
from ImagingS.core.brush import Brushes, Brush
from ImagingS.core.geometry import Geometry


class GeometryDrawing(Drawing):
    def __init__(self) -> None:
        super().__init__()
        self.stroke = Pen()
        self.fill = Brushes.White()

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
        for point in self.geometry.stroke(self.stroke):
            context.point(point,
                          self.stroke.brush.color_at(point, self.boundingArea))
        for point in self.geometry.fill():
            context.point(point, self.fill.color_at(point, self.boundingArea))
