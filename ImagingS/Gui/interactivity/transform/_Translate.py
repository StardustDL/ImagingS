from typing import Union

from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QKeyEvent, QPainterPath

from ImagingS.drawing import DrawingGroup
from ImagingS.geometry import Geometry
from ImagingS.Gui import converters
from ImagingS.transform import TranslateTransform

from . import TransformInteractivity


class TranslateTransformInteractivity(TransformInteractivity[TranslateTransform]):
    def __init__(self, target: Union[DrawingGroup, Geometry], transform: TranslateTransform) -> None:
        super().__init__(target, transform)

    def start(self) -> None:
        self._hasStarted = False
        self._isShift = False
        super().start()

    def _updateData(self) -> None:
        self.transform.delta = self._end - self._start

        path = QPainterPath()
        s = converters.qpoint(self._start)
        t = converters.qpoint(self._end)
        path.addEllipse(s, 3, 3)
        path.moveTo(s)
        path.lineTo(t)
        self._viewItem.setPath(path)

    def _setEndPoint(self, point: QPointF) -> None:
        if self._isShift:
            tp = converters.point(point)
            delta = tp - self._start
            if abs(delta.x) <= abs(delta.y):
                delta.x = 0
            else:
                delta.y = 0
            self._end = self._start + delta
        else:
            self._end = converters.point(point)

    def onMouseRelease(self, point: QPointF) -> None:
        if not self._hasStarted:
            self._start = converters.point(point)
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
