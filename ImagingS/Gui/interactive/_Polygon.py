from PyQt5.QtCore import QPointF
from . import Interactive
from ImagingS.core.geometry import Polygon
from ImagingS.Gui.graphics import converters


class PolygonInteractive(Interactive):
    def __init__(self, drawing: Polygon) -> None:
        super().__init__()
        self.drawing = drawing

    def start(self) -> None:
        super().start()
        self._hasStarted = False

    def onMouseRelease(self, point: QPointF) -> None:
        super().onMouseRelease(point)
        if not self._hasStarted:
            self.drawing.vertexes.append(converters.convert_qpoint(point))
            self.drawing.vertexes.append(
                converters.convert_qpoint(point))  # for next vertex
            self._hasStarted = True
        else:
            self.drawing.vertexes.append(
                converters.convert_qpoint(point))  # for next vertex

    def onMouseMove(self, point: QPointF) -> None:
        super().onMouseMove(point)
        if self._hasStarted:
            self.drawing.vertexes[-1] = converters.convert_qpoint(point)
            self._needRender()

    def onMouseDoubleClick(self, point: QPointF) -> None:
        super().onMouseDoubleClick(point)
        self.drawing.refresh_boundingArea()
        self._end()
