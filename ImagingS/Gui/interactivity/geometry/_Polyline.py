from PyQt5.QtCore import QPointF

from ImagingS import Size
from ImagingS.drawing import GeometryDrawing
from ImagingS.geometry import PolylineGeometry
from ImagingS.Gui import converters

from . import GeometryInteractivity


class PolylineInteractivity(GeometryInteractivity[PolylineGeometry]):
    def __init__(self, target: GeometryDrawing, geometry: PolylineGeometry, size: Size) -> None:
        super().__init__(target, geometry, size)

    def start(self) -> None:
        self._hasStarted = False
        super().start()

    def onMouseRelease(self, point: QPointF) -> None:
        if not self._hasStarted:
            self.geometry.vertexes.append(converters.point(point))
            self.geometry.vertexes.append(
                converters.point(point))  # for next vertex
            self._hasStarted = True
        else:
            self.geometry.vertexes.append(
                converters.point(point))  # for next vertex
        super().onMouseRelease(point)

    def onMouseMove(self, point: QPointF) -> None:
        if self._hasStarted:
            self.geometry.vertexes[-1] = converters.point(point)
            self.update()
        super().onMouseMove(point)

    def onMouseDoubleClick(self, point: QPointF) -> None:
        if len(self.geometry.vertexes) > 1:
            self.geometry.vertexes.remove(self.geometry.vertexes[-1])
        self.update()
        self.end(True)
        super().onMouseDoubleClick(point)
