from PyQt5.QtCore import QPointF
from . import Interactive
from ImagingS.core.geometry import Line
from ImagingS.Gui.graphics import converters


class LineInteractive(Interactive):
    def __init__(self, drawing: Line) -> None:
        super().__init__()
        self.drawing = drawing

    def start(self) -> None:
        super().start()
        self._hasStarted = False

    def onMouseRelease(self, point: QPointF) -> None:
        super().onMouseRelease(point)
        if not self._hasStarted:
            self.drawing.start = converters.convert_qpoint(point)
            self._hasStarted = True
        else:
            self.drawing.end = converters.convert_qpoint(point)
            self.drawing.refresh_boundingArea()
            self._end()

    def onMouseMove(self, point: QPointF) -> None:
        super().onMouseMove(point)
        if self._hasStarted:
            self.drawing.end = converters.convert_qpoint(point)
            self._needRender()
