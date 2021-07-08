from typing import Optional, Union

from ImagingS.geometry import LineGeometry, LineClipAlgorithm
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPathItem
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QColor, QKeyEvent, QPainterPath, QPen

from ImagingS import Rect, Size
from ImagingS.drawing import DrawingGroup
from ImagingS.Gui import converters

from . import Interactivity


class RectClipInteractivity(Interactivity):
    def __init__(self, target: Union[DrawingGroup, LineGeometry], size: Size) -> None:
        super().__init__()
        self._target = target

        self._viewItem = QGraphicsPathItem()
        pen = QPen(QColor("purple"))
        pen.setWidth(1)
        pen.setStyle(Qt.DashLine)
        pen.setCapStyle(Qt.RoundCap)
        self._viewItem.setPen(pen)

    @property
    def viewItem(self) -> Optional[QGraphicsItem]:
        return self._viewItem

    @property
    def target(self) -> Union[DrawingGroup, LineGeometry]:
        return self._target

    @property
    def clip(self) -> Optional[Rect]:
        return self._clip

    @clip.setter
    def clip(self, value: Optional[Rect]) -> None:
        self._clip = value

    @property
    def clipAlgorithm(self) -> LineClipAlgorithm:
        return self._clipAlgorithm

    @clipAlgorithm.setter
    def clipAlgorithm(self, value: LineClipAlgorithm) -> None:
        self._clipAlgorithm = value

    def start(self) -> None:
        self._hasStarted = False
        self._isShift = False
        super().start()

    def update(self) -> None:
        self.target.refreshBounds()
        super().update()

    def _updateData(self) -> None:
        if isinstance(self.target, LineGeometry):
            # self.target.clip = Rect.fromPoints(self._start, self._end)
            pass
        else:
            assert False  # not support generic clip for now TODO
        path = QPainterPath()
        path.addRect(converters.qrect(Rect.fromPoints(self._start, self._end)))
        self._viewItem.setPath(path)

    def end(self, success: bool) -> None:
        if not success:
            if isinstance(self.target, LineGeometry):
                self.clip = None
            else:
                self.target.clip = None
        else:
            if isinstance(self.target, LineGeometry):
                self.clip = Rect.fromPoints(self._start, self._end)
            else:
                self.target.clip = Rect.fromPoints(self._start, self._end)
            
        super().end(success)

    def _setEndPoint(self, point: QPointF) -> None:
        if self._isShift:
            tp = converters.point(point)
            delta = tp - self._start
            if abs(delta.x) <= abs(delta.y):
                delta.y = delta.x
            else:
                delta.x = delta.y
            self._end = self._start + delta
        else:
            self._end = converters.point(point)

    def onMouseRelease(self, point: QPointF) -> None:
        if not self._hasStarted:
            self._start = converters.point(point)
            self._hasStarted = True
        else:
            self._setEndPoint(point)
            self._updateData()
            self.end(True)
        super().onMouseRelease(point)

    def onMouseMove(self, point: QPointF) -> None:
        if self._hasStarted:
            self._setEndPoint(point)
            self._updateData()
            self.update()
        super().onMouseMove(point)

    def onKeyPress(self, key: QKeyEvent) -> None:
        if key.key() == Qt.Key_Shift:
            self._isShift = True
        if key.key() == Qt.Key_Escape:
            self.end(False)
        super().onKeyPress(key)

    def onKeyRelease(self, key: QKeyEvent) -> None:
        if key.key() == Qt.Key_Shift:
            self._isShift = False
        super().onKeyRelease(key)
