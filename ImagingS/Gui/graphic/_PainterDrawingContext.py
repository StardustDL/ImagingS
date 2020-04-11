from PyQt5.QtGui import QPainter

from ImagingS import Color, Point, Rect
from ImagingS.drawing import DrawingContext
from ImagingS.Gui import converters


class PainterDrawingContext(DrawingContext):
    def __init__(self, painter: QPainter, rect: Rect):
        super().__init__()
        self._painter = painter
        self._rect = rect

    def point(self, position: Point, color: Color) -> None:
        self._painter.setPen(converters.qcolor(color))
        self._painter.drawPoint(converters.qpoint(position))

    def rect(self) -> Rect:
        return self._rect
