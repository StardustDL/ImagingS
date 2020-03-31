from __future__ import annotations
from typing import List, Optional
from ImagingS.document import Document
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QObject


class Application(QObject):
    documentChanged = pyqtSignal()

    def __init__(self, argv: List[str]):
        super().__init__()
        self._app = QApplication(argv)
        self._document: Optional[Document] = None
        Application._current = self

    @property
    def app(self) -> QApplication:
        return self._app

    @property
    def document(self) -> Optional[Document]:
        return self._document

    @document.setter
    def document(self, doc: Optional[Document]) -> None:
        self._document = doc
        self.documentChanged.emit()

    def run(self) -> int:
        return self.app.exec_()
    
    @classmethod
    def current(cls) -> Application:
        return cls._current
