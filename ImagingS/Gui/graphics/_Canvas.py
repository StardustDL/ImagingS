from typing import Dict, Optional
from ImagingS.core.drawing import Drawing
from . import DrawingItem

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtCore import QSizeF, QPointF, QRectF


class Canvas(QGraphicsView):
    def __init__(self, parent):
        scene = QGraphicsScene(parent)
        super().__init__(scene, parent)

        self.items: Dict[str, DrawingItem] = {}
        self._active_item: Optional[DrawingItem] = None

        self._sceneBorder = QGraphicsRectItem()
        self.scene().addItem(self._sceneBorder)

    def resize(self, size: QSizeF):
        self.scene().setSceneRect(QRectF(QPointF(), size))
        self._sceneBorder.setRect(self.scene().sceneRect())
        # self.setFixedSize(QSize(size.width() + 5, size.height() + 5))
        self.update()

    def add(self, drawing: Drawing) -> None:
        item = DrawingItem(drawing, self.size())
        self.items[drawing.id] = item
        self.scene().addItem(item)
        self.update()

    def remove(self, name: str) -> None:
        if name not in self.items:
            return
        item = self.items[name]
        self.scene().removeItem(item)
        del self.items[name]
        self.update()

    def select(self, name: Optional[str]) -> None:
        if name is None:
            if self._active_item is not None:
                self._active_item.is_active = False
                self._active_item = None
                self.update()
            return
        if name not in self.items:
            return
        if self._active_item is not None:
            self._active_item.is_active = False
        item = self.items[name]
        self._active_item = item
        item.is_active = True
        self.update()

    def clear(self) -> None:
        for draw in self.items.values():
            self.scene().removeItem(draw)
        self.items.clear()
