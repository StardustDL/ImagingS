from ImagingS.core.drawing import Drawing
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsLineItem
from typing import Optional
from . import Interactive
from ImagingS.core import Point
from ImagingS.core.transform import SkewTransform
from ImagingS.Gui.graphics import converters
import math


class SkewTransformInteractive(Interactive):
    def __init__(self, drawing: Drawing) -> None:
        super().__init__()
        self.drawing = drawing
        self.transform = SkewTransform()
        self.drawing.transform = self.transform
        self._view_item = QGraphicsLineItem()

    @property
    def view_item(self) -> Optional[QGraphicsItem]:
        return self._view_item

    def start(self) -> None:
        self._hasStarted = False
        super().start()

    def __set(self, delta: Point) -> None:
        delta.x = min(delta.x, 360)
        delta.x = max(delta.x, -360)
        delta.y = min(delta.y, 360)
        delta.y = max(delta.y, -360)
        self.transform.angle_x = (delta.x / 360) * math.pi / 2
        self.transform.angle_y = (delta.y / 360) * math.pi / 2

    def onMouseRelease(self, point: QPointF) -> None:
        super().onMouseRelease(point)
        if not self._hasStarted:
            self._begin_point = converters.convert_qpoint(point)
            self.transform.center = self._begin_point
            self._view_item.setLine(
                self._begin_point.x, self._begin_point.y, self._begin_point.x, self._begin_point.y)
            self._hasStarted = True
        else:
            self._end_point = converters.convert_qpoint(point)
            self._view_item.setLine(
                self._begin_point.x, self._begin_point.y, self._end_point.x, self._end_point.y)
            delta = self._end_point - self._begin_point
            self.__set(delta)
            self._end(self.S_Success)

    def onMouseMove(self, point: QPointF) -> None:
        super().onMouseMove(point)
        if self._hasStarted:
            self._end_point = converters.convert_qpoint(point)
            self._view_item.setLine(
                self._begin_point.x, self._begin_point.y, self._end_point.x, self._end_point.y)
            delta = self._end_point - self._begin_point
            self.__set(delta)
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
