from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QKeyEvent

from ImagingS import Rect, Size
from ImagingS.drawing import GeometryDrawing
from ImagingS.geometry import RectangleGeometry
from ImagingS.Gui import converters

from . import GeometryInteractivity


class RectangleInteractivity(GeometryInteractivity[RectangleGeometry]):
    def __init__(self, target: GeometryDrawing, geometry: RectangleGeometry, size: Size) -> None:
        super().__init__(target, geometry, size)

    def start(self) -> None:
        self._hasStarted = False
        self._isShift = False
        super().start()

    def _setGeometry(self) -> None:
        self.geometry.rect = Rect.fromPoints(self._beginPoint, self._endPoint)

    def _setEndPoint(self, point: QPointF) -> None:
        if self._isShift:
            tp = converters.point(point)
            delta = tp - self._beginPoint
            if abs(delta.x) <= abs(delta.y):
                delta.y = delta.x
            else:
                delta.x = delta.y
            self._endPoint = self._beginPoint + delta
        else:
            self._endPoint = converters.point(point)

    def onMouseRelease(self, point: QPointF) -> None:
        if not self._hasStarted:
            self._beginPoint = converters.point(point)
            self._hasStarted = True
        else:
            self._setEndPoint(point)
            self._setGeometry()
            self.update()
            self.end(True)
        super().onMouseRelease(point)

    def onMouseMove(self, point: QPointF) -> None:
        if self._hasStarted:
            self._setEndPoint(point)
            self._setGeometry()
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
