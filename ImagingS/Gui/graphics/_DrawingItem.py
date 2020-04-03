from ImagingS.core import Point, RectArea
from ImagingS.core.drawing import Drawing
from . import PainterDrawingContext
from . import converters

from PyQt5.QtWidgets import QGraphicsItem, QWidget, QStyleOptionGraphicsItem
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QRectF, QSizeF
from typing import Optional


class DrawingItem(QGraphicsItem):
    def __init__(self, drawing: Drawing, size: QSizeF, parent: QGraphicsItem = None):
        super().__init__(parent)
        self._drawing = drawing
        self._size = size
        self.is_active = False

    @property
    def drawing(self) -> Drawing:
        return self._drawing

    @property
    def is_active(self) -> bool:
        return self._is_active

    @is_active.setter
    def is_active(self, value: bool) -> None:
        self._is_active = value

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        context = PainterDrawingContext(
            painter, RectArea.create(Point(), converters.convert_qsize(self._size)))
        self.drawing.render(context)
        if self.is_active:
            painter.setPen(QColor(255, 0, 0))
            painter.drawRect(self.boundingRect())

    def boundingRect(self) -> QRectF:
        area = self.drawing.boundingArea
        return converters.convert_rect_area(area)
