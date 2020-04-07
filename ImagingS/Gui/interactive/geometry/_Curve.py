from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QKeyEvent

from ImagingS.core.geometry import CurveGeometry
from ImagingS.Gui import converters

from .. import Interactive


class CurveInteractive(Interactive):
    def __init__(self, drawing: Curve) -> None:
        super().__init__()
        self.drawing = drawing

    def start(self) -> None:
        self._hasStarted = False
        super().start()

    def onMouseRelease(self, point: QPointF) -> None:
        super().onMouseRelease(point)
        if not self._hasStarted:
            self.drawing.control_points.append(
                converters.convert_qpoint(point))
            self.drawing.control_points.append(
                converters.convert_qpoint(point))  # for next vertex
            self._hasStarted = True
        else:
            self.drawing.control_points.append(
                converters.convert_qpoint(point))  # for next vertex

    def onMouseMove(self, point: QPointF) -> None:
        super().onMouseMove(point)
        if self._hasStarted:
            self.drawing.control_points[-1] = converters.convert_qpoint(point)
            self._needRender()

    def onMouseDoubleClick(self, point: QPointF) -> None:
        super().onMouseDoubleClick(point)
        self.drawing.refresh_boundingArea()
        self._end(self.S_Success)

    def onKeyPress(self, key: QKeyEvent) -> None:
        super().onKeyPress(key)
        if key.key() == Qt.Key_Escape:
            self._needRender()
            self._end(self.S_Failed)
