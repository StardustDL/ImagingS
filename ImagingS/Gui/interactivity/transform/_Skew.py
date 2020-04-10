import math
from typing import Union

from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QKeyEvent, QPainterPath

from ImagingS import Point, fsign
from ImagingS.drawing import DrawingGroup
from ImagingS.geometry import Geometry
from ImagingS.Gui import converters
from ImagingS.transform import SkewTransform

from . import TransformInteractivity


class SkewTransformInteractivity(TransformInteractivity[SkewTransform]):
    def __init__(self, target: Union[DrawingGroup, Geometry], transform: SkewTransform) -> None:
        super().__init__(target, transform)

    def start(self) -> None:
        self._hasStarted = False
        self._isShift = False
        super().start()

    def _updateData(self) -> None:  # y-axis: zero rad
        R = 50
        BOUND = math.pi / 2 - math.pi / 6
        ax, ay = self.transform.angle

        if hasattr(self, "_second"):
            delta = self._second - self._center
            ay = abs(math.atan2(abs(delta.x), abs(delta.y))) * \
                fsign(delta.x)  # x-axis positive means > 0
            ay = max(min(ay, BOUND), -BOUND)
        else:
            delta = self._first - self._center
            ax = abs(math.atan2(abs(delta.x), abs(delta.y))) * \
                fsign(delta.x)  # x-axis positive means > 0
            ax = max(min(ax, BOUND), -BOUND)

        self.transform.angle = (ax, ay)

        path = QPainterPath()
        s = converters.qpoint(self._center)
        rect = QRectF(s.x() - R, s.y() - R, 2*R, 2*R)
        dax, day = ax / math.pi * 180, ay / math.pi * 180
        path.moveTo(s)
        path.arcTo(rect, 90.0, -dax)  # x-axis positive means > 0
        path.lineTo(s)
        path.arcTo(rect, -90.0, day)  # x-axis positive means > 0
        path.lineTo(s)
        self._viewItem.setPath(path)

    def _setPoint(self, point: QPointF) -> Point:
        if self._isShift:
            tp = converters.point(point)
            delta = tp - self._center
            if abs(delta.x) <= abs(delta.y):
                delta.x = 0
            else:
                delta.y = 0
            return self._center + delta
        else:
            return converters.point(point)

    def onMouseRelease(self, point: QPointF) -> None:
        if not self._hasStarted:
            self._center = converters.point(point)
            self.transform.center = self._center
            self._first = self._center
            self._hasStarted = True
        else:
            if hasattr(self, "_second"):
                self._second = self._setPoint(point)
                self._updateData()
                self.end(True)
            else:
                self._first = self._setPoint(point)
                self._second = self._center
                self._updateData()
        super().onMouseRelease(point)

    def onMouseMove(self, point: QPointF) -> None:
        if self._hasStarted:
            if hasattr(self, "_second"):
                self._second = self._setPoint(point)
            else:
                self._first = self._setPoint(point)
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
