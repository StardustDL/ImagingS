from enum import Enum, unique
from typing import Optional

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

import ImagingS.Gui.ui as ui
from ImagingS.document import Document

from . import CodePage, CodePageState, VisualPage, VisualPageState


@unique
class DocumentEditorState(Enum):
    Disable = 0
    Visual = 1
    Code = 2


class DocumentEditor(QWidget, ui.DocumentEditor):
    documentCommitted = pyqtSignal(Document, str)
    stateChanged = pyqtSignal()
    messaged = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setupVisual()
        self.setupCode()

        self.code.documentCommitted.connect(self.code_documentCommitted)
        self.visual.documentCommitted.connect(self.visual_documentCommitted)

        self.setEnabled(False)

    def setupCode(self) -> None:
        self.code = CodePage()
        self.code.setObjectName("code")
        self.grdCode.addWidget(self.code, 0, 0, 1, 1)
        self.code.messaged.connect(self.visualCode_messaged)

    def setupVisual(self) -> None:
        self.visual = VisualPage()
        self.visual.setObjectName("visual")
        self.grdVisual.addWidget(self.visual, 0, 0, 1, 1)
        self.visual.messaged.connect(self.visualCode_messaged)

    @property
    def document(self) -> Optional[Document]:
        if hasattr(self, "_document"):
            return self._document
        else:
            return None

    @property
    def state(self) -> DocumentEditorState:
        if hasattr(self, "_document"):
            if self.swgMain.currentIndex() == 0:
                return DocumentEditorState.Visual
            else:
                return DocumentEditorState.Code
        else:
            return DocumentEditorState.Disable

    def enable(self, doc: Document) -> None:
        assert self.state is DocumentEditorState.Disable
        self.setEnabled(True)
        self._document = doc
        self.switchVisual()

    def disable(self) -> None:
        assert self.state is not DocumentEditorState.Disable
        if hasattr(self, "_document"):
            del self._document
        if self.visual.state is not VisualPageState.Disable:
            self.visual.disable()
        if self.code.state is not CodePageState.Disable:
            self.code.disable()
        self.setEnabled(False)
        self.stateChanged.emit()

    def fresh(self) -> None:
        state = self.state
        if state is DocumentEditorState.Disable:
            return
        elif state is DocumentEditorState.Visual:
            self.visual.fresh()
        elif state is DocumentEditorState.Code:
            self.code.fresh()

    def switchCode(self) -> bool:
        if self.document is None:
            return True
        if self.code.state is not CodePageState.Disable:
            return True
        if self.visual.state is VisualPageState.Normal:
            self.visual.disable()
        elif self.visual.state is VisualPageState.Interactive:
            self.messaged.emit("Still in interactive mode.")
            return False
        self.code.enable(self.document)
        self.swgMain.setCurrentIndex(1)
        self.stateChanged.emit()
        return True

    def switchVisual(self) -> bool:
        if self.document is None:
            return True
        if self.visual.state is not VisualPageState.Disable:
            return True
        if self.code.state is CodePageState.Normal:
            self.code.disable()
        elif self.code.state is CodePageState.Changed:
            self.messaged.emit("Code changes not committed.")
            return False
        self.visual.enable(self.document)
        self.swgMain.setCurrentIndex(0)
        self.stateChanged.emit()
        return True

    def visualCode_messaged(self, message: str) -> None:
        self.messaged.emit(message)

    def code_documentCommitted(self, doc: Document, message: str):
        self._document = doc
        self.documentCommitted.emit(doc, message)

    def visual_documentCommitted(self, doc: Document, message: str):
        self._document = doc
        self.documentCommitted.emit(doc, message)
