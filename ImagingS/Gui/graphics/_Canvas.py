from typing import Dict, Optional
from ImagingS.core.drawing import Drawing
from ImagingS.Gui.interactive import Interactive
from . import DrawingItem

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtCore import QSizeF, QPointF, QRectF
from PyQt5.QtGui import QMouseEvent


class Canvas(QGraphicsView):
    def __init__(self, parent):
        scene = QGraphicsScene(parent)
        super().__init__(scene, parent)
        self.setMouseTracking(True)

        self.items: Dict[str, DrawingItem] = {}
        self._active_item: Optional[DrawingItem] = None

        self._sceneBorder = QGraphicsRectItem()
        self.scene().addItem(self._sceneBorder)
        self.interactive = None

    @property
    def interactive(self) -> Optional[Interactive]:
        return self._interative

    @interactive.setter
    def interactive(self, value: Optional[Interactive]) -> None:
        self._interative = value
        if self._interative is not None:
            self._interative.start()
            self._interative.ended.connect(self._interative_ended)

    def _interative_ended(self):
        if self._interative is not None:
            self._after_interactive()
        self.interactive = None

    def rerender(self) -> None:
        self.updateScene([self.sceneRect()])

    def resize(self, size: QSizeF):
        self.scene().setSceneRect(QRectF(QPointF(), size))
        self._sceneBorder.setRect(self.scene().sceneRect())

        draws = self.items.values()

        self.clear()
        for item in draws:
            self.add(item)

    def add(self, drawing: Drawing) -> None:
        item = DrawingItem(drawing, self.scene().sceneRect().size())
        self.items[drawing.id] = item
        self.scene().addItem(item)
        self.rerender()

    def remove(self, name: str) -> None:
        if name not in self.items:
            return
        item = self.items[name]
        self.scene().removeItem(item)
        del self.items[name]
        self.rerender()

    def select(self, name: Optional[str]) -> None:
        if name is None:
            if self._active_item is not None:
                self._active_item.is_active = False
                self._active_item = None
                self.rerender()
            return
        if name not in self.items:
            return
        if self._active_item is not None:
            self._active_item.is_active = False
        item = self.items[name]
        self._active_item = item
        item.is_active = True
        self.rerender()

    def clear(self) -> None:
        for draw in self.items.values():
            self.scene().removeItem(draw)
        self.items.clear()
        self.rerender()

    def _after_interactive(self) -> None:
        if self.interactive is None:
            return
        if self.interactive.isNeedRender:
            self.rerender()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        if self.interactive is not None:
            self.interactive.onMousePress(pos)
            self._after_interactive()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        if self.interactive is not None:
            self.interactive.onMouseMove(pos)
            self._after_interactive()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        if self.interactive is not None:
            self.interactive.onMouseRelease(pos)
            self._after_interactive()
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        if self.interactive is not None:
            self.interactive.onMouseDoubleClick(pos)
            self._after_interactive()
        super().mouseDoubleClickEvent(event)
