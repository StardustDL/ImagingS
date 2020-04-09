from enum import Enum, unique
from io import StringIO
from typing import Optional

import qtawesome as qta
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

import ImagingS.Gui.ui as ui
from ImagingS.document import Document, DocumentFormat
from ImagingS.Gui.models import PropertyModel


@unique
class CodePageState(Enum):
    Disable = 0,
    Normal = 1,
    Changed = 2


class CodePage(QWidget, ui.CodePage):
    uploaded = pyqtSignal(Document)
    messaged = pyqtSignal(str)
    stateChanged = pyqtSignal(CodePageState)

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setupIcon()

        self.modelCode = PropertyModel(self)
        self.trvCode.setModel(self.modelCode)

        self.tetCode.textChanged.connect(self.tetCode_textChanged)
        self.actBuild.triggered.connect(self.actBuild_triggered)
        self.actRestore.triggered.connect(self.actRestore_triggered)
        self.actUpload.triggered.connect(self.actUpload_triggered)

        self.setEnabled(False)
        self._state = CodePageState.Disable

    def setupIcon(self) -> None:
        self.actBuild.setIcon(qta.icon("mdi.play"))
        self.actRestore.setIcon(qta.icon("mdi.restore"))
        self.actUpload.setIcon(qta.icon("mdi.upload"))
        self.setWindowIcon(qta.icon("mdi.code-tags"))

    def _showdoc(self, doc: Document) -> None:
        io = StringIO()
        doc.save(io, DocumentFormat.RAW)
        self.tetCode.setText(io.getvalue())
        self.modelCode.fresh(doc)
        width = self.trvCode.size().width() / 2
        if width > 0:
            self.trvCode.setColumnWidth(0, width)
            self.trvCode.setColumnWidth(1, width)
        self.trvCode.expandAll()

    def _loaddoc(self) -> Optional[Document]:
        assert self.state is not CodePageState.Disable

        io = StringIO(self.code)
        try:
            tdoc = Document.load(io, DocumentFormat.RAW)
            return tdoc
        except Exception:
            return None

    def enable(self, doc: Document) -> None:
        assert self.state is CodePageState.Disable
        self.setEnabled(True)
        self._document = doc
        self._showdoc(self._document)
        self._state = CodePageState.Normal

    def disable(self) -> None:
        assert self.state is not CodePageState.Disable
        if hasattr(self, "_document"):
            del self._document
        self.tetCode.setText("")
        self.modelCode.fresh()
        self.setEnabled(False)
        self._state = CodePageState.Disable

    @property
    def code(self) -> str:
        return self.tetCode.toPlainText()

    @property
    def state(self) -> CodePageState:
        return self._state

    def tetCode_textChanged(self) -> None:
        self._state = CodePageState.Changed

    def actBuild_triggered(self) -> None:
        doc = self._loaddoc()

        if doc is None:
            self.modelCode.fresh()
            self.messaged.emit("Loading document from code FAILED.")
        else:
            self._showdoc(doc)

    def actRestore_triggered(self) -> None:
        self._showdoc(self._document)

    def actUpload_triggered(self) -> None:
        doc = self._loaddoc()
        if doc is None:
            self.modelCode.fresh()
            self.messaged.emit("Loading document from code FAILED.")
        else:
            self._document = doc
            self._showdoc(doc)
            self.uploaded.emit(doc)
            self._state = CodePageState.Normal
