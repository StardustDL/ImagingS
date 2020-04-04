from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QKeyEvent
from .. import Interactive
from ImagingS.core.geometry import Line
from ImagingS.Gui.graphics import converters


class LineInteractive(Interactive):
    def __init__(self, drawing: Line) -> None:
        super().__init__()
        self.drawing = drawing

    def start(self) -> None:
        self._hasStarted = False
        super().start()

    def onMouseRelease(self, point: QPointF) -> None:
        super().onMouseRelease(point)
        if not self._hasStarted:
            self.drawing.start = converters.convert_qpoint(point)
            self._hasStarted = True
        else:
            self.drawing.end = converters.convert_qpoint(point)
            self.drawing.refresh_boundingArea()
            self._end(self.S_Success)

    def onMouseMove(self, point: QPointF) -> None:
        super().onMouseMove(point)
        if self._hasStarted:
            self.drawing.end = converters.convert_qpoint(point)
            self._needRender()

    def onKeyPress(self, key: QKeyEvent) -> None:
        super().onKeyPress(key)
        if key.key() == Qt.Key_Escape:
            self.drawing.end = self.drawing.start
            self._needRender()
            self._end(self.S_Failed)
