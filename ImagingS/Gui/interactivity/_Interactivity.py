from __future__ import annotations

from enum import Enum, unique
from typing import Optional

from PyQt5.QtCore import QObject, QPointF, pyqtSignal
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QGraphicsItem


@unique
class InteractivityState(Enum):
    Pending = 1,
    Running = 2,
    Success = 3,
    Failed = 4


class Interactivity(QObject):
    started = pyqtSignal(QObject)
    ended = pyqtSignal(QObject)
    updated = pyqtSignal(QObject)

    def __init__(self) -> None:
        super().__init__()
        self._isNeedRender = False
        self._state = InteractivityState.Pending

    def start(self) -> None:  # will emit event, so call at the end in subclass
        self._state = InteractivityState.Running
        self.started.emit(self)

    def end(self, success: bool) -> None:
        if success:
            self._state = InteractivityState.Success
        else:
            self._state = InteractivityState.Failed
        self.ended.emit(self)

    def update(self) -> None:
        self.updated.emit(self)

    @property
    def viewItem(self) -> Optional[QGraphicsItem]:
        return None

    @property
    def state(self) -> InteractivityState:
        return self._state

    def onMousePress(self, point: QPointF) -> None: pass

    def onMouseMove(self, point: QPointF) -> None: pass

    def onMouseRelease(self, point: QPointF) -> None: pass

    def onMouseDoubleClick(self, point: QPointF) -> None: pass

    def onKeyPress(self, key: QKeyEvent) -> None: pass

    def onKeyRelease(self, key: QKeyEvent) -> None: pass
