from enum import Enum, unique
from io import StringIO

import qtawesome as qta
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

import ImagingS.Gui.ui as ui
from ImagingS.document import Document, DocumentFormat
from ImagingS.Gui import icons
from ImagingS.Gui.models import PropertyModel


@unique
class CodePageState(Enum):
    Disable = 0,
    Normal = 1,
    Changed = 2


def _clonedoc(doc: Document) -> Document:
    io = StringIO()
    doc.save(io, DocumentFormat.RAW)
    io = StringIO(io.getvalue())
    return Document.load(io, DocumentFormat.RAW)


class CodePage(QWidget, ui.CodePage):
    documentCommitted = pyqtSignal(Document, str)
    messaged = pyqtSignal(str)
    stateChanged = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setupIcon()

        self.modelCode = PropertyModel(self)
        self.modelCode.onlyEditable = True
        self.trvTree.setModel(self.modelCode)
        self.modelCode.changed.connect(self.modelCode_changed)
        self.tetCode.textChanged.connect(self.tetCode_textChanged)

        self.actRestore.triggered.connect(self.actRestore_triggered)
        self.actCommit.triggered.connect(self.actCommit_triggered)
        self.actSwitch.triggered.connect(self.actSwitch_triggered)

        self.swgMain.setCurrentIndex(0)

        self.setEnabled(False)
        self._state = CodePageState.Disable

    def setupIcon(self) -> None:
        self.actRestore.setIcon(qta.icon("mdi.restore"))
        self.actCommit.setIcon(qta.icon("mdi.check"))
        self.actSwitch.setIcon(icons.fileTree)
        self.setWindowIcon(icons.code)

    def switchCode(self, force: bool = False) -> None:
        if self.swgMain.currentIndex() == 0 and not force:
            return

        io = StringIO()
        self._curdocument.save(io, DocumentFormat.RAW)
        self.tetCode.setText(io.getvalue())
        self.actSwitch.setIcon(icons.fileTree)
        self.swgMain.setCurrentIndex(0)

    def switchTree(self, force: bool = False) -> None:
        if self.swgMain.currentIndex() == 1 and not force:
            return

        io = StringIO(self.tetCode.toPlainText())
        try:
            tdoc = Document.load(io, DocumentFormat.RAW)
        except Exception:
            self.messaged.emit("Some syntax errors in code")
            return

        self._curdocument = tdoc
        self.modelCode.fresh(self._curdocument)
        width = round(self.trvTree.size().width() / 2)
        if width > 0:
            self.trvTree.setColumnWidth(0, width)
            self.trvTree.setColumnWidth(1, width)
        self.trvTree.expandAll()

        self.actSwitch.setIcon(icons.code)
        self.swgMain.setCurrentIndex(1)

    def _setState(self, value: CodePageState) -> None:
        self._state = value
        if self.state is CodePageState.Changed:
            self.actRestore.setEnabled(True)
            self.actCommit.setEnabled(True)
        else:
            self.actRestore.setEnabled(False)
            self.actCommit.setEnabled(False)
        self.stateChanged.emit()

    def fresh(self) -> None:
        if self.state is not CodePageState.Normal:
            return

        if self.swgMain.currentIndex() == 0:
            self.switchCode(True)
        else:
            self.switchTree(True)
        self._setState(CodePageState.Normal)

    def enable(self, doc: Document) -> None:
        assert self.state is CodePageState.Disable
        self.setEnabled(True)
        self._document = doc
        self._curdocument = _clonedoc(self._document)
        self.switchCode(True)
        self._setState(CodePageState.Normal)

    def disable(self) -> None:
        assert self.state is not CodePageState.Disable
        if hasattr(self, "_document"):
            del self._document
        self.tetCode.setText("")
        self.modelCode.fresh()
        self.setEnabled(False)
        self._setState(CodePageState.Disable)

    @property
    def state(self) -> CodePageState:
        return self._state

    def modelCode_changed(self) -> None:
        self._setState(CodePageState.Changed)

    def tetCode_textChanged(self) -> None:
        self._setState(CodePageState.Changed)

    def actRestore_triggered(self) -> None:
        self._curdocument = _clonedoc(self._document)
        self.switchCode(True)
        self._setState(CodePageState.Normal)

    def actCommit_triggered(self) -> None:
        if self.swgMain.currentIndex() == 0 and self.state is CodePageState.Changed:
            io = StringIO(self.tetCode.toPlainText())
            try:
                tdoc = Document.load(io, DocumentFormat.RAW)
            except Exception:
                self.messaged.emit("Some syntax errors in code")
                return

            self._curdocument = tdoc

        self.modelCode.fresh(self._curdocument)
        self._document = self._curdocument
        self.actRestore.trigger()
        self.documentCommitted.emit(self._document, "Change Code")

    def actSwitch_triggered(self) -> None:
        if self.swgMain.currentIndex() == 0:
            self.switchTree()
        else:
            self.switchCode()
