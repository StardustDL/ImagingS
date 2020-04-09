from PyQt5.QtCore import QPointF

from ImagingS import Size
from ImagingS.drawing import GeometryDrawing
from ImagingS.geometry import LineGeometry
from ImagingS.Gui import converters

from . import GeometryInteractive


class LineInteractive(GeometryInteractive[LineGeometry]):
    def __init__(self, target: GeometryDrawing, geometry: LineGeometry, size: Size) -> None:
        super().__init__(target, geometry, size)

    def start(self) -> None:
        self._hasStarted = False
        super().start()

    def onMouseRelease(self, point: QPointF) -> None:
        if not self._hasStarted:
            self.geometry.start = converters.point(point)
            self._hasStarted = True
        else:
            self.geometry.end = converters.point(point)
            self.target.refreshBoundingRect()
            self.end(True)
        super().onMouseRelease(point)

    def onMouseMove(self, point: QPointF) -> None:
        if self._hasStarted:
            self.geometry.end = converters.point(point)
            self.update()
        super().onMouseMove(point)
