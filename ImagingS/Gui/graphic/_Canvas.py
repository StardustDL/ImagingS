from typing import Dict, Optional

from PyQt5.QtCore import QPointF, QRectF, QSizeF
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene, QGraphicsView

from ImagingS.drawing import Drawing

from . import DrawingItem


class Canvas(QGraphicsView):
    def __init__(self, parent):
        scene = QGraphicsScene(parent)
        super().__init__(scene, parent)
        self.setMouseTracking(True)

        self.items: Dict[str, DrawingItem] = {}
        self._active_item: Optional[DrawingItem] = None

        self._sceneBorder = QGraphicsRectItem()
        self.scene().addItem(self._sceneBorder)

    def rerender(self) -> None:
        self.updateScene([self.sceneRect()])

    def resize(self, size: QSizeF):
        self.scene().setSceneRect(QRectF(QPointF(), size))
        self._sceneBorder.setRect(self.scene().sceneRect())

        draws = self.items.values()

        self.clear()
        for item in draws:
            self.add(item.drawing)

    def add(self, drawing: Drawing) -> None:
        item = DrawingItem(drawing, self.scene().sceneRect().size())
        self.items[drawing.id] = item
        self.scene().addItem(item)
        self.rerender()

    def remove(self, name: str) -> None:
        if name not in self.items:
            return
        item = self.items[name]
        del self.items[name]
        self.scene().removeItem(item)
        self.rerender()

    def select(self, name: Optional[str] = None) -> None:
        if self._active_item is not None:
            self._active_item.deactivate()
        if name is None or name not in self.items:
            self._active_item = None
        else:
            item = self.items[name]
            item.activate()
            self._active_item = item
        self.rerender()

    def clear(self) -> None:
        for draw in self.items.values():
            self.scene().removeItem(draw)
        self.items.clear()
        self.rerender()


"""
    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        if self.interactive is not None:
            inter = self.interactive
            inter.onMousePress(pos)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        if self.interactive is not None:
            inter = self.interactive
            inter.onMouseMove(pos)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        if self.interactive is not None:
            inter = self.interactive
            inter.onMouseRelease(pos)
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        if self.interactive is not None:
            inter = self.interactive
            inter.onMouseDoubleClick(pos)
        super().mouseDoubleClickEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if self.interactive is not None:
            inter = self.interactive
            inter.onKeyPress(event)
        elif event.key() == Qt.Key_F5:
            self.rerender()
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if self.interactive is not None:
            inter = self.interactive
            inter.onKeyRelease(event)
        super().keyReleaseEvent(event)
"""
