from math import floor
from typing import Union

from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QKeyEvent, QPainterPath

from ImagingS.drawing import DrawingGroup
from ImagingS.geometry import Geometry
from ImagingS.Gui import converters
from ImagingS.transform import ScaleTransform

from . import TransformInteractivity


class ScaleTransformInteractivity(TransformInteractivity[ScaleTransform]):
    def __init__(self, target: Union[DrawingGroup, Geometry], transform: ScaleTransform) -> None:
        super().__init__(target, transform)

    def start(self) -> None:
        self._hasStarted = False
        self._isShift = False
        super().start()

    def _updateData(self) -> None:
        D = 40  # point distance
        BOUND = 3.0

        delta = self._end - self._start
        fx, fy = (max(min(delta.x / D, BOUND), -BOUND),
                  max(min(delta.y / D, BOUND), -BOUND))
        rfx, rfy = fx, fy
        if rfx < 0:
            rfx = 1.0 / (1+abs(rfx))
        else:
            rfx += 1
        if rfy < 0:
            rfy = 1.0 / (1+abs(rfy))
        else:
            rfy += 1
        self.transform.factor = rfx, rfy

        path = QPainterPath()
        s = converters.qpoint(self._start)
        t = QPointF(s.x()+fx*D, s.y()+fy*D)
        fbound = floor(BOUND)
        for i in range(1, fbound + 1):
            path.addEllipse(QPointF(s.x()+i*D, s.y()),
                            (fbound + i)/2, (fbound + i)/2)
            path.addEllipse(QPointF(s.x()-i*D, s.y()),
                            (fbound - i)/2, (fbound - i)/2)
            path.addEllipse(QPointF(s.x(), s.y()+i*D),
                            (fbound + i)/2, (fbound + i)/2)
            path.addEllipse(QPointF(s.x(), s.y()-i*D),
                            (fbound - i)/2, (fbound - i)/2)

        tx = QPointF(s.x()+fx*D, s.y())
        ty = QPointF(s.x(), s.y()+fy*D)
        path.addEllipse(s, 3, 3)
        path.addEllipse(t, 3, 3)

        path.moveTo(s)
        path.lineTo(QPointF(s.x()+BOUND*D, s.y()))
        path.moveTo(s)
        path.lineTo(QPointF(s.x()-BOUND*D, s.y()))
        path.moveTo(s)
        path.lineTo(QPointF(s.x(), s.y()+BOUND*D))
        path.moveTo(s)
        path.lineTo(QPointF(s.x(), s.y()-BOUND*D))
        path.moveTo(t)
        path.lineTo(tx)
        path.moveTo(t)
        path.lineTo(ty)
        self._viewItem.setPath(path)

    def _setEndPoint(self, point: QPointF) -> None:
        if self._isShift:
            tp = converters.point(point)
            delta = tp - self._start
            if abs(delta.x) <= abs(delta.y):  # equal factor(x,y) are same
                delta.y = delta.x
            else:
                delta.x = delta.y
            self._end = self._start + delta
        else:
            self._end = converters.point(point)

    def onMouseRelease(self, point: QPointF) -> None:
        if not self._hasStarted:
            self._start = converters.point(point)
            self.transform.center = self._start
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
