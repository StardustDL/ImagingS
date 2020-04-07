from io import StringIO
from typing import Optional

import qtawesome as qta
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

import ImagingS.Gui.ui as ui
from ImagingS.document import Document, DocumentFormat
from ImagingS.Gui.models import PropertyModel


class CodePage(QWidget, ui.CodePage):
    uploaded = pyqtSignal()
    messaged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupIcon()

        self.modelCode = PropertyModel(self)
        self.trvCode.setModel(self.modelCode)

        self.actBuild.triggered.connect(self.actBuild_triggered)
        self.actRestore.triggered.connect(self.actRestore_triggered)
        self.actUpload.triggered.connect(self.actUpload_triggered)

        self.document = None

    def setupIcon(self):
        self.actBuild.setIcon(qta.icon("mdi.play"))
        self.actRestore.setIcon(qta.icon("mdi.restore"))
        self.actUpload.setIcon(qta.icon("mdi.upload"))
        self.setWindowIcon(qta.icon("mdi.code-tags"))

    def fresh(self) -> None:
        if self.document is None:
            self.tetCode.setText("")
            self.modelCode.fresh()
        else:
            io = StringIO()
            self.document.save(io, DocumentFormat.RAW)
            self.tetCode.setText(io.getvalue())
            self.modelCode.fresh(self.document)
            width = self.trvCode.size().width() / 2
            if width > 0:
                self.trvCode.setColumnWidth(0, width)
                self.trvCode.setColumnWidth(1, width)
            self.trvCode.expandAll()

    def upload(self) -> None:
        doc = self.load_document()
        self.modelCode.fresh(doc)
        if doc is None:
            self.messaged.emit("Loading document from code FAILED.")
        self.uploaded.emit()

    @property
    def document(self) -> Optional[Document]:
        return self._document

    @document.setter
    def document(self, value: Optional[Document]) -> None:
        self._document = value
        self.fresh()

    @property
    def code(self) -> str:
        return self.tetCode.toPlainText()

    def load_document(self) -> Optional[Document]:
        io = StringIO(self.code)
        try:
            tdoc = Document.load(io, DocumentFormat.RAW)
            return tdoc
        except Exception:
            return None

    def actBuild_triggered(self) -> None:
        doc = self.load_document()
        self.modelCode.fresh(doc)
        if doc is None:
            self.messaged.emit("Loading document from code FAILED.")

    def actRestore_triggered(self) -> None:
        self.fresh()

    def actUpload_triggered(self) -> None:
        self.upload()
