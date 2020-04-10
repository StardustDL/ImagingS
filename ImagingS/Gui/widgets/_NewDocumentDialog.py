import qtawesome as qta
from PyQt5.QtWidgets import QDialog

import ImagingS.Gui.ui as ui
from ImagingS import Size


class NewDocumentDialog(QDialog, ui.NewDocumentDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setupIcon()

    def setupIcon(self) -> None:
        self.setWindowIcon(qta.icon("mdi.file"))

    @property
    def documentSize(self) -> Size:
        return Size(self.sbxWidth.value(), self.sbxHeight.value())
