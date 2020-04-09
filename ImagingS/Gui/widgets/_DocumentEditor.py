from enum import Enum, unique
from typing import Optional

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

import ImagingS.Gui.ui as ui
from ImagingS.document import Document
from ImagingS.Gui import icons

from . import CodePage, CodePageState, VisualPage, VisualPageState


@unique
class DocumentEditorState(Enum):
    Disable = 0
    Visual = 1
    Code = 2


class DocumentEditor(QWidget, ui.DocumentEditor):
    documentChanged = pyqtSignal(Document)
    messaged = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setupVisual()
        self.setupCode()
        self.setupIcon()

        self.code.uploaded.connect(self.code_uploaded)
        self.tbxMain.currentChanged.connect(self.tbxMain_currentChanged)

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

    def setupIcon(self) -> None:
        self.tbxMain.setItemIcon(0, icons.visual)
        self.tbxMain.setItemIcon(1, icons.code)

    @property
    def document(self) -> Optional[Document]:
        if hasattr(self, "_document"):
            return self._document
        else:
            return None

    @property
    def state(self) -> DocumentEditorState:
        if hasattr(self, "_document"):
            if self.tbxMain.currentIndex() == 0:
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

    def switchCode(self) -> bool:
        if self.document is None:
            return True
        if self.code.state is not CodePageState.Disable:
            return True
        if self.visual.state is VisualPageState.Normal:
            self.visual.disable()
        elif self.visual.state is VisualPageState.Interactive:
            self.messaged("Still in interactive mode.")
            return False
        self.code.enable(self.document)
        self.tbxMain.setCurrentIndex(1)
        return True

    def switchVisual(self) -> bool:
        if self.document is None:
            return True
        if self.visual.state is not VisualPageState.Disable:
            return True
        if self.code.state is CodePageState.Normal:
            self.code.disable()
        elif self.code.state is CodePageState.Changed:
            self.messaged.emit("Code changes not uploaded.")
            return False
        self.visual.enable(self.document)
        self.tbxMain.setCurrentIndex(0)
        return True

    def visualCode_messaged(self, message: str) -> None:
        self.messaged.emit(message)

    def code_uploaded(self, doc: Document):
        self.documentChanged.emit(doc)

    def tbxMain_currentChanged(self, index):
        if index == 0:
            if not self.switchVisual():
                self.tbxMain.setCurrentIndex(1)
        else:
            if not self.switchCode():
                self.tbxMain.setCurrentIndex(0)
