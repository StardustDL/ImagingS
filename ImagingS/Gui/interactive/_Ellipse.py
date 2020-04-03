from ImagingS.core import Size
from PyQt5.QtCore import QPointF
from . import Interactive
from ImagingS.core.geometry import Ellipse
from ImagingS.Gui.graphics import converters


class EllipseInteractive(Interactive):
    def __init__(self, drawing: Ellipse) -> None:
        super().__init__()
        self.drawing = drawing

    def start(self) -> None:
        super().start()
        self._hasStarted = False

    def onMouseRelease(self, point: QPointF) -> None:
        super().onMouseRelease(point)
        if not self._hasStarted:
            self.drawing.area.origin = converters.convert_qpoint(point)
            self._hasStarted = True
        else:
            delta = converters.convert_qpoint(point) - self.drawing.area.origin
            self.drawing.area.size = Size.create(delta.x, delta.y)
            self.drawing.refresh_boundingArea()
            self._end()

    def onMouseMove(self, point: QPointF) -> None:
        super().onMouseMove(point)
        if self._hasStarted:
            delta = converters.convert_qpoint(point) - self.drawing.area.origin
            self.drawing.area.size = Size.create(delta.x, delta.y)
            self._needRender()
