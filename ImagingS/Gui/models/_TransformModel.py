from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel

from ImagingS.core.transform import Transform, TransformGroup, TranslateTransform, ScaleTransform, RotateTransform, MatrixTransform, SkewTransform
from ImagingS.Gui import icons


class TransformModel(QStandardItemModel):
    NAME = 0

    def __init__(self, parent) -> None:
        super().__init__(0, 1, parent)
        self.setHeaderData(TransformModel.NAME, Qt.Horizontal, "Name")

    def append(self, transform: Transform) -> None:
        fitem = None
        if isinstance(transform, TranslateTransform):
            fitem = QStandardItem(icons.translateTransform, "Translate")
        elif isinstance(transform, SkewTransform):
            fitem = QStandardItem(icons.skewTransform, "Skew")
        elif isinstance(transform, RotateTransform):
            fitem = QStandardItem(icons.rotateTransform, "Rotate")
        elif isinstance(transform, ScaleTransform):
            fitem = QStandardItem(icons.scaleTransform, "Scale")
        elif isinstance(transform, MatrixTransform):
            fitem = QStandardItem(icons.matrix, "Matrix")
        if fitem:
            fitem.setEditable(False)
            self.appendRow(fitem)
        else:
            raise Exception("Unsupport transform")

    def clear_items(self) -> None:
        self.removeRows(0, self.rowCount())
