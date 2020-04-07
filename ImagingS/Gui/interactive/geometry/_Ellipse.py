from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QKeyEvent

from ImagingS import Size
from ImagingS.geometry import Ellipse
from ImagingS.Gui.graphics import converters

from .. import Interactive


class EllipseInteractive(Interactive):
    def __init__(self, drawing: Ellipse) -> None:
        super().__init__()
        self.drawing = drawing

    def start(self) -> None:
        self._hasStarted = False
        super().start()

    def onMouseRelease(self, point: QPointF) -> None:
        super().onMouseRelease(point)
        if not self._hasStarted:
            self.drawing.area.origin = converters.convert_qpoint(point)
            self._hasStarted = True
        else:
            delta = converters.convert_qpoint(point) - self.drawing.area.origin
            self.drawing.area.size = Size.create(delta.x, delta.y)
            self.drawing.refresh_boundingArea()
            self._end(self.S_Success)

    def onMouseMove(self, point: QPointF) -> None:
        super().onMouseMove(point)
        if self._hasStarted:
            delta = converters.convert_qpoint(point) - self.drawing.area.origin
            self.drawing.area.size = Size.create(delta.x, delta.y)
            self._needRender()

    def onKeyPress(self, key: QKeyEvent) -> None:
        super().onKeyPress(key)
        if key.key() == Qt.Key_Escape:
            self._needRender()
            self._end(self.S_Failed)
