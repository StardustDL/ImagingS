from ImagingS.core import Point, Rect
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
            painter, Rect.create(Point(), converters.convert_qsize(self._size)))
        self.drawing.render(context)
        if self.is_active:
            painter.setPen(QColor(255, 0, 0))
            area = self.drawing.boundingArea
            painter.drawRect(converters.convert_rect_area(area))

    def boundingRect(self) -> QRectF:  # must be efficient
        return QRectF(0, 0, self._size.width(), self._size.height())  # to fix prepareGeometryChange bug
        self.prepareGeometryChange()  # important!!!
        area = self.drawing.boundingArea
        return QRectF(area.origin.x - 1, area.origin.y - 1, area.size.width + 2, area.size.height + 2)
