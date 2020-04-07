from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QKeyEvent

from ImagingS.geometry import Polygon
from ImagingS.Gui.graphics import converters

from .. import Interactive


class PolygonInteractive(Interactive):
    def __init__(self, drawing: Polygon) -> None:
        super().__init__()
        self.drawing = drawing

    def start(self) -> None:
        self._hasStarted = False
        super().start()

    def onMouseRelease(self, point: QPointF) -> None:
        super().onMouseRelease(point)
        if not self._hasStarted:
            self.drawing.vertexes.append(converters.convert_qpoint(point))
            self.drawing.vertexes.append(
                converters.convert_qpoint(point))  # for next vertex
            self.drawing.refresh_boundingArea()
            self._hasStarted = True
        else:
            self.drawing.vertexes.append(
                converters.convert_qpoint(point))  # for next vertex
            self.drawing.refresh_boundingArea()

    def onMouseMove(self, point: QPointF) -> None:
        super().onMouseMove(point)
        if self._hasStarted:
            self.drawing.vertexes[-1] = converters.convert_qpoint(point)
            self.drawing.refresh_boundingArea()
            self._needRender()

    def onMouseDoubleClick(self, point: QPointF) -> None:
        super().onMouseDoubleClick(point)
        self.drawing.refresh_boundingArea()
        self._end(self.S_Success)

    def onKeyPress(self, key: QKeyEvent) -> None:
        super().onKeyPress(key)
        if key.key() == Qt.Key_Escape:
            self.drawing.vertexes.clear()
            self.drawing.refresh_boundingArea()
            self._needRender()
            self._end(self.S_Failed)
