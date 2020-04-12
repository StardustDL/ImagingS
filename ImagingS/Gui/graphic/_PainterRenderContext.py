from PyQt5.QtGui import QPainter

from ImagingS import Color, Point, Rect
from ImagingS.drawing import RenderContext
from ImagingS.Gui import converters


class PainterRenderContext(RenderContext):
    def __init__(self, painter: QPainter, bounds: Rect):
        super().__init__()
        self._painter = painter
        self._bounds = bounds

    def _point(self, position: Point, color: Color) -> None:
        self._painter.setPen(converters.qcolor(color))
        self._painter.drawPoint(converters.qpoint(position))

    def bounds(self) -> Rect:
        return self._bounds
