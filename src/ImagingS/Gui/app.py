from __future__ import annotations

from typing import List

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication


class Application(QObject):

    def __init__(self, argv: List[str]):
        super().__init__()
        self._app = QApplication(argv)
        Application._current = self

    @property
    def app(self) -> QApplication:
        return self._app

    def run(self) -> int:
        return self.app.exec_()

    @classmethod
    def current(cls) -> Application:
        return cls._current
