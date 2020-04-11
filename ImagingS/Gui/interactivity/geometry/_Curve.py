from PyQt5.QtCore import QPointF

from ImagingS import Size
from ImagingS.drawing import GeometryDrawing
from ImagingS.geometry import CurveGeometry
from ImagingS.Gui import converters

from . import GeometryInteractivity


class CurveInteractivity(GeometryInteractivity[CurveGeometry]):
    def __init__(self, target: GeometryDrawing, geometry: CurveGeometry, size: Size) -> None:
        super().__init__(target, geometry, size)

    def start(self) -> None:
        self._hasStarted = False
        super().start()

    def onMouseRelease(self, point: QPointF) -> None:
        if not self._hasStarted:
            self.geometry.controlPoints.append(converters.point(point))
            self.geometry.controlPoints.append(
                converters.point(point))  # for next vertex
            self._hasStarted = True
        else:
            self.geometry.controlPoints.append(
                converters.point(point))  # for next vertex
        super().onMouseRelease(point)

    def onMouseMove(self, point: QPointF) -> None:
        if self._hasStarted:
            self.geometry.controlPoints[-1] = converters.point(point)
            self.update()
        super().onMouseMove(point)

    def onMouseDoubleClick(self, point: QPointF) -> None:
        if len(self.geometry.controlPoints) > 1:
            self.geometry.controlPoints.remove(self.geometry.controlPoints[-1])
        self.update()
        self.end(True)
        super().onMouseDoubleClick(point)
