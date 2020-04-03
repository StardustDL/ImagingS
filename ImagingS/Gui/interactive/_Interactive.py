from PyQt5.QtCore import QPointF
from PyQt5.QtCore import pyqtSignal, QObject


class Interactive(QObject):
    started = pyqtSignal()
    ended = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self._isNeedRender = False

    def start(self) -> None:
        self.started.emit()

    @property
    def isNeedRender(self) -> bool:
        return self._isNeedRender

    def _needRender(self) -> None:
        self._isNeedRender = True

    def _end(self) -> None:
        self.ended.emit()

    def onMousePress(self, point: QPointF) -> None:
        self._isNeedRender = False

    def onMouseMove(self, point: QPointF) -> None:
        self._isNeedRender = False

    def onMouseRelease(self, point: QPointF) -> None:
        self._isNeedRender = False

    def onMouseDoubleClick(self, point: QPointF) -> None:
        self._isNeedRender = False
