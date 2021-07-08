from typing import Optional

from PyQt5.QtCore import QRectF, QSizeF
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget

from ImagingS import Point, Rect
from ImagingS.drawing import Drawing, GeometryDrawing
from ImagingS.geometry import Geometry
from ImagingS.Gui import converters

from . import PainterRenderContext


class DrawingItem(QGraphicsItem):
    def __init__(self, drawing: Drawing, size: QSizeF, parent: Optional[QGraphicsItem] = None):
        super().__init__(parent)
        self._drawing = drawing
        self._size = size
        self._is_active = False

    @property
    def drawing(self) -> Drawing:
        return self._drawing

    def activate(self) -> None:
        if isinstance(self.drawing, GeometryDrawing):
            self.drawing.geometry.refreshBounds()
        self._is_active = True

    def deactivate(self) -> None:
        self._is_active = False

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = None) -> None:
        context = PainterRenderContext(
            painter, Rect(Point(), converters.size(self._size)))
        self.drawing.render(context)
        if self._is_active:
            painter.setPen(QColor(255, 0, 0))
            rect = self.drawing.bounds
            painter.drawRect(converters.qrect(rect))

    def boundingRect(self) -> QRectF:  # must be efficient
        # to fix prepareGeometryChange bug
        return QRectF(0, 0, self._size.width(), self._size.height())
        # self.prepareGeometryChange()  # important!!!
        # rect = self.drawing.bounds
        # return QRectF(rect.origin.x - 1, rect.origin.y - 1, rect.size.width + 2, rect.size.height + 2)


# class DrawingGroupItem(QGraphicsItemGroup):
#     def __init__(self, drawing: DrawingGroup, size: QSizeF, parent: QGraphicsItem = None):
#         super().__init__(parent)
#         self._drawing = drawing
#         self._size = size
#         self._is_active = False

#     @property
#     def drawing(self) -> DrawingGroup:
#         return self._drawing

#     def activate(self) -> None:
#         self._is_active = True

#     def deactivate(self) -> None:
#         self._is_active = False

#     def fresh(self) -> None:
#         for item in self.childItems:
#             self.removeFromGroup(item)
#         for di in self.drawing.children:
#             item = None
#             if isinstance(di, DrawingGroup):
#                 item = DrawingGroupItem(di, self._size)
#             else:
#                 item = DrawingItem(di, self._size)
#             self.addToGroup(item)

#     def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = None) -> None:
#         super().paint(painter, option, widget)
#         if self._is_active:
#             painter.setPen(QColor(255, 0, 0))
#             rect = self.drawing.bounds
#             painter.drawRect(converters.qrect(rect))
