from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QKeyEvent

from ImagingS import Size
from ImagingS.drawing import GeometryDrawing
from ImagingS.geometry import LineGeometry
from ImagingS.Gui import converters

from . import GeometryInteractivity


class LineInteractivity(GeometryInteractivity[LineGeometry]):
    def __init__(self, target: GeometryDrawing, geometry: LineGeometry, size: Size) -> None:
        super().__init__(target, geometry, size)

    def start(self) -> None:
        self._hasStarted = False
        self._isShift = False
        super().start()

    def _setEndPoint(self, point: QPointF) -> None:
        if self._isShift:
            tp = converters.point(point)
            delta = tp - self.geometry.start
            if abs(delta.x) <= abs(delta.y):
                delta.x = 0
            else:
                delta.y = 0
            self.geometry.end = self.geometry.start + delta
        else:
            self.geometry.end = converters.point(point)

    def onMouseRelease(self, point: QPointF) -> None:
        if not self._hasStarted:
            self.geometry.start = converters.point(point)
            self._hasStarted = True
        else:
            self._setEndPoint(point)
            self.update()
            self.end(True)
        super().onMouseRelease(point)

    def onMouseMove(self, point: QPointF) -> None:
        if self._hasStarted:
            self._setEndPoint(point)
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
