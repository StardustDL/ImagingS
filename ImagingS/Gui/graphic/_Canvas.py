from typing import Dict, Optional

from PyQt5.QtCore import QPointF, QRectF, QSizeF, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QKeyEvent, QMouseEvent, QPainterPath, QPen
from PyQt5.QtWidgets import (QAction, QGraphicsPathItem, QGraphicsRectItem,
                             QGraphicsScene, QGraphicsView)

from ImagingS.drawing import Drawing
from ImagingS.Gui import icons
from ImagingS.Gui.interactivity import Interactivity

from . import DrawingItem


class Canvas(QGraphicsView):
    mouseMoved = pyqtSignal(QPointF)
    mouseReleased = pyqtSignal(QPointF)

    def __init__(self, parent):
        scene = QGraphicsScene(parent)
        super().__init__(scene, parent)
        self.setupActions()
        self.setContextMenuPolicy(Qt.ActionsContextMenu)

        self.interactivity = None

        self.items: Dict[str, DrawingItem] = {}
        self._active_item: Optional[DrawingItem] = None

        self._sceneBorder = QGraphicsRectItem()
        self._sceneGrid = QGraphicsPathItem()
        self._sceneGrid.setVisible(False)
        self._sceneGrid.setPen(QPen(QColor("lightgray")))
        self.scene().addItem(self._sceneBorder)
        self.scene().addItem(self._sceneGrid)

        self.setMouseTracking(True)

    def setupActions(self):
        self.actRerender = QAction(self)
        self.actRerender.setObjectName("actactRerender")
        self.actRerender.triggered.connect(self.actRerender_triggered)
        self.actRerender.setIcon(icons.refresh)
        self.actRerender.setText("Rerender")
        self.actRerender.setShortcut("F5")
        self.addAction(self.actRerender)

        self.actGrid = QAction(self)
        self.actGrid.setObjectName("actGrid")
        self.actGrid.triggered.connect(self.actGrid_triggered)
        self.actGrid.setIcon(icons.grid)
        self.actGrid.setCheckable(True)
        self.actGrid.setChecked(False)
        self.actGrid.setText("Gird")
        self.actGrid.setShortcut("F4")
        self.addAction(self.actGrid)

    @property
    def interactivity(self) -> Optional[Interactivity]:
        return self._interactivity

    @interactivity.setter
    def interactivity(self, value: Optional[Interactivity]) -> None:
        self._interactivity = value

    def rerender(self) -> None:
        self.updateScene([self.sceneRect()])

    def resize(self, size: QSizeF):
        self.scene().setSceneRect(QRectF(QPointF(), size))
        self._sceneBorder.setRect(self.scene().sceneRect())

        gridPath = QPainterPath()
        D = 80
        for x in range(0, round(size.width()), D):
            gridPath.moveTo(QPointF(x, 0))
            gridPath.lineTo(QPointF(x, size.height()))
        for y in range(0, round(size.height()), D):
            gridPath.moveTo(QPointF(0, y))
            gridPath.lineTo(QPointF(size.width(), y))
        self._sceneGrid.setPath(gridPath)

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

    def actRerender_triggered(self) -> None:
        self.rerender()

    def actGrid_triggered(self) -> None:
        if self.actGrid.isChecked():
            self._sceneGrid.setVisible(True)
        else:
            self._sceneGrid.setVisible(False)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        if self.interactivity is not None:
            inter = self.interactivity
            inter.onMousePress(pos)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        if self.interactivity is not None:
            inter = self.interactivity
            inter.onMouseMove(pos)
        self.mouseMoved.emit(pos)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        if self.interactivity is not None:
            inter = self.interactivity
            inter.onMouseRelease(pos)
        self.mouseReleased.emit(pos)
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        if self.interactivity is not None:
            inter = self.interactivity
            inter.onMouseDoubleClick(pos)
        super().mouseDoubleClickEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if self.interactivity is not None:
            inter = self.interactivity
            inter.onKeyPress(event)
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if self.interactivity is not None:
            inter = self.interactivity
            inter.onKeyRelease(event)
        super().keyReleaseEvent(event)
