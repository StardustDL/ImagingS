from ImagingS.core.drawing import Drawing
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsLineItem
from typing import Optional
from . import Interactive
from ImagingS.core.transform import TranslateTransform
from ImagingS.Gui.graphics import converters


class TranslateTransformInteractive(Interactive):
    def __init__(self, drawing: Drawing) -> None:
        super().__init__()
        self.drawing = drawing
        self.transform = TranslateTransform()
        self.drawing.transform = self.transform
        self._view_item = QGraphicsLineItem()

    @property
    def view_item(self) -> Optional[QGraphicsItem]:
        return self._view_item

    def start(self) -> None:
        self._hasStarted = False
        super().start()

    def onMouseRelease(self, point: QPointF) -> None:
        super().onMouseRelease(point)
        if not self._hasStarted:
            self._begin_point = converters.convert_qpoint(point)
            self._view_item.setLine(
                self._begin_point.x, self._begin_point.y, self._begin_point.x, self._begin_point.y)
            self._hasStarted = True
        else:
            self._end_point = converters.convert_qpoint(point)
            self._view_item.setLine(
                self._begin_point.x, self._begin_point.y, self._end_point.x, self._end_point.y)
            self.transform.delta = self._end_point - self._begin_point
            self._end(self.S_Success)

    def onMouseMove(self, point: QPointF) -> None:
        super().onMouseMove(point)
        if self._hasStarted:
            self._end_point = converters.convert_qpoint(point)
            self._view_item.setLine(
                self._begin_point.x, self._begin_point.y, self._end_point.x, self._end_point.y)
            self.transform.delta = self._end_point - self._begin_point
            self.drawing.refresh_boundingArea()
            self._needRender()

    def onKeyPress(self, key: QKeyEvent) -> None:
        super().onKeyPress(key)
        if key.key() == Qt.Key_Escape:
            self._view_item.setLine(
                self._begin_point.x, self._begin_point.y, self._begin_point.x, self._begin_point.y)
            self.drawing.refresh_boundingArea()
            self._needRender()
            self._end(self.S_Failed)
