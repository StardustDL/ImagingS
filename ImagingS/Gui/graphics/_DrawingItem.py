from typing import Optional

from PyQt5.QtCore import QRectF, QSizeF
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget

from ImagingS import Point, Rect
from ImagingS.drawing import Drawing
from ImagingS.Gui import converters

from . import PainterDrawingContext


class DrawingItem(QGraphicsItem):
    def __init__(self, drawing: Drawing, size: QSizeF, parent: QGraphicsItem = None):
        super().__init__(parent)
        self._drawing = drawing
        self._size = size
        self._is_active = False

    @property
    def drawing(self) -> Drawing:
        return self._drawing

    def activate(self) -> None:
        self._is_active = True

    def deactivate(self) -> None:
        self._is_active = False

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        context = PainterDrawingContext(
            painter, Rect.create(Point(), converters.size(self._size)))
        self.drawing.render(context)
        if self._is_active:
            painter.setPen(QColor(255, 0, 0))
            area = self.drawing.boundingArea
            painter.drawRect(converters.qrect(area))

    def boundingRect(self) -> QRectF:  # must be efficient
        # to fix prepareGeometryChange bug
        return QRectF(0, 0, self._size.width(), self._size.height())
        # self.prepareGeometryChange()  # important!!!
        # area = self.drawing.boundingArea
        # return QRectF(area.origin.x - 1, area.origin.y - 1, area.size.width + 2, area.size.height + 2)
