from PyQt5.QtGui import QPainter

from ImagingS.core import Color, Point, Rect
from ImagingS.core.drawing import DrawingContext
from ImagingS.Gui import converters


class PainterDrawingContext(DrawingContext):
    def __init__(self, painter: QPainter, area: Rect):
        super().__init__()
        self._painter = painter
        self._area = area

    def point(self, position: Point, color: Color) -> None:
        self._painter.setPen(converters.convert_color(color))
        self._painter.drawPoint(position.x, position.y)

    def area(self) -> Rect:
        return self._area
