import math
from typing import Union

from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QKeyEvent, QPainterPath

from ImagingS.drawing import DrawingGroup
from ImagingS.geometry import Geometry
from ImagingS.Gui import converters
from ImagingS.transform import RotateTransform

from . import TransformInteractivity


class RotateTransformInteractivity(TransformInteractivity[RotateTransform]):
    def __init__(self, target: Union[DrawingGroup, Geometry], transform: RotateTransform) -> None:
        super().__init__(target, transform)

    def start(self) -> None:
        self._hasStarted = False
        self._isShift = False
        super().start()

    def _updateData(self) -> None:
        R = 50

        delta = self._end - self._center
        self.transform.angle = math.atan2(delta.y, delta.x)

        path = QPainterPath()
        s = converters.qpoint(self._center)
        rect = QRectF(s.x() - R, s.y() - R, 2*R, 2*R)
        path.moveTo(s)
        path.arcTo(rect, 0, -self.transform.angle / math.pi * 180)
        path.lineTo(s)
        self._viewItem.setPath(path)

    def _setEndPoint(self, point: QPointF) -> None:
        if self._isShift:
            tp = converters.point(point)
            delta = tp - self._center
            if abs(delta.x) <= abs(delta.y):
                delta.x = 0
            else:
                delta.y = 0
            self._end = self._center + delta
        else:
            self._end = converters.point(point)

    def onMouseRelease(self, point: QPointF) -> None:
        if not self._hasStarted:
            self._center = converters.point(point)
            self.transform.center = self._center
            self._hasStarted = True
        else:
            self._setEndPoint(point)
            self._updateData()
            self.end(True)
        super().onMouseRelease(point)

    def onMouseMove(self, point: QPointF) -> None:
        if self._hasStarted:
            self._setEndPoint(point)
            self._updateData()
            self.update()
        super().onMouseMove(point)

    def onKeyPress(self, key: QKeyEvent) -> None:
        if key.key() == Qt.Key_Shift:
            self._isShift = True
        super().onKeyPress(key)

    def onKeyRelease(self, key: QKeyEvent) -> None:
        if key.key() == Qt.Key_Shift:
            self._isShift = False
        super().onKeyRelease(key)
