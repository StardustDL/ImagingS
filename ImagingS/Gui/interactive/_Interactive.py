from __future__ import annotations

from enum import IntEnum, unique
from typing import Optional

from PyQt5.QtCore import QObject, QPointF, pyqtSignal
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QGraphicsItem


@unique
class InteractiveState(IntEnum):
    Pending = 1,
    Running = 2,
    Success = 3,
    Failed = 4


class Interactive(QObject):
    started = pyqtSignal(QObject)
    ended = pyqtSignal(QObject)

    def __init__(self) -> None:
        super().__init__()
        self._isNeedRender = False
        self._state = InteractiveState.Pending

    def start(self) -> None:  # will emit event, so call at the end in subclass
        self._state = InteractiveState.Running
        self.started.emit(self)

    def end(self, success: bool) -> None:
        if success:
            self._state = InteractiveState.Success
        else:
            self._state = InteractiveState.Failed
        self.ended.emit(self)

    @property
    def view_item(self) -> Optional[QGraphicsItem]:
        return None

    @property
    def state(self) -> InteractiveState:
        return self._state

    @property
    def is_need_render(self) -> bool:
        return self._is_need_render

    def _need_render(self) -> None:
        self._is_need_render = True

    def onMousePress(self, point: QPointF) -> None:
        self._is_need_render = False

    def onMouseMove(self, point: QPointF) -> None:
        self._is_need_render = False

    def onMouseRelease(self, point: QPointF) -> None:
        self._is_need_render = False

    def onMouseDoubleClick(self, point: QPointF) -> None:
        self._is_need_render = False

    def onKeyPress(self, key: QKeyEvent) -> None:
        self._is_need_render = False

    def onKeyRelease(self, key: QKeyEvent) -> None:
        self._is_need_render = False
