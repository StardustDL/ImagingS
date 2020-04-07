from typing import Dict, Optional

from PyQt5.QtCore import QPointF, QRectF, QSizeF, Qt
from PyQt5.QtGui import QKeyEvent, QMouseEvent
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene, QGraphicsView

from ImagingS.drawing import Drawing
from ImagingS.Gui.interactive import Interactive

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
        self.interactive = None

    @property
    def interactive(self) -> Optional[Interactive]:
        return self._interactive

    @interactive.setter
    def interactive(self, value: Optional[Interactive]) -> None:
        if value is not None:
            value.started.connect(self._interactive_started)
            value.ended.connect(self._interactive_ended)
            value.start()
        self._interactive = value

    def _interactive_force_end(self):
        if self._interactive is None:
            return
        self._interactive_ended(self._interactive)

    def _interactive_started(self, inter: Interactive):
        if inter.view_item is not None:
            self.scene().addItem(inter.view_item)
            self.rerender()

    def _interactive_ended(self, inter: Interactive):
        if inter.view_item is not None:
            self.scene().removeItem(inter.view_item)
            self.rerender()

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

    def _after_interactive(self, inter: Interactive) -> None:
        if inter.isNeedRender:
            self.rerender()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        if self.interactive is not None:
            inter = self.interactive
            inter.onMousePress(pos)
            self._after_interactive(inter)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        if self.interactive is not None:
            inter = self.interactive
            inter.onMouseMove(pos)
            self._after_interactive(inter)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        if self.interactive is not None:
            inter = self.interactive
            inter.onMouseRelease(pos)
            self._after_interactive(inter)
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        if self.interactive is not None:
            inter = self.interactive
            inter.onMouseDoubleClick(pos)
            self._after_interactive(inter)
        super().mouseDoubleClickEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if self.interactive is not None:
            inter = self.interactive
            inter.onKeyPress(event)
            self._after_interactive(inter)
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if self.interactive is not None:
            inter = self.interactive
            inter.onKeyRelease(event)
            self._after_interactive(inter)
        elif event.key() == Qt.Key_F5:
            self.rerender()
        super().keyReleaseEvent(event)
