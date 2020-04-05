from __future__ import annotations
from typing import Optional
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QKeyEvent


class Interactive(QObject):
    S_Success, S_Failed = range(2)

    started = pyqtSignal(QObject)
    ended = pyqtSignal(QObject)

    def __init__(self) -> None:
        super().__init__()
        self._isNeedRender = False
        self._state = self.S_Failed

    def start(self) -> None:  # will emit event, so call at the end in subclass
        self._state = self.S_Failed
        self.started.emit(self)

    @property
    def view_item(self) -> Optional[QGraphicsItem]:
        return None

    @property
    def state(self) -> int:
        return self._state

    @property
    def isNeedRender(self) -> bool:
        return self._isNeedRender

    def _needRender(self) -> None:
        self._isNeedRender = True

    def _end(self, state: int) -> None:
        self._state = state
        self.ended.emit(self)

    def onMousePress(self, point: QPointF) -> None:
        self._isNeedRender = False

    def onMouseMove(self, point: QPointF) -> None:
        self._isNeedRender = False

    def onMouseRelease(self, point: QPointF) -> None:
        self._isNeedRender = False

    def onMouseDoubleClick(self, point: QPointF) -> None:
        self._isNeedRender = False

    def onKeyPress(self, key: QKeyEvent) -> None:
        self._isNeedRender = False

    def onKeyRelease(self, key: QKeyEvent) -> None:
        self._isNeedRender = False
