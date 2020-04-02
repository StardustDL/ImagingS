from ImagingS.core.drawing import DrawingContext
from ImagingS.core import Point, Color, Size

from PyQt5.QtGui import QPainter
from . import converters


class PainterDrawingContext(DrawingContext):
    def __init__(self, painter: QPainter, size: Size):
        super().__init__()
        self._painter = painter
        self._size = size

    def point(self, position: Point, color: Color) -> None:
        self._painter.setPen(converters.convert_color(color))
        self._painter.drawPoint(position.x, position.y)

    @property
    def size(self) -> Size:
        return self._size
