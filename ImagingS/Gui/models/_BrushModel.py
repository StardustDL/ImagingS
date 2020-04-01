from ImagingS.core import Color
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QIcon, QPixmap, QColor, QStandardItem
from ImagingS.core.brush import Brush, SolidBrush


def _get_color_icon(color: Color) -> QIcon:
    pixmap = QPixmap(32, 32)
    pixmap.fill(QColor(color.r, color.g, color.b))
    return QIcon(pixmap)


class BrushModel(QStandardItemModel):
    NAME = 0

    def __init__(self, parent) -> None:
        super().__init__(0, 1, parent)
        self.setHeaderData(BrushModel.NAME, Qt.Horizontal, "Name")

    def append(self, brush: Brush) -> None:
        if isinstance(brush, SolidBrush):
            fitem = QStandardItem(_get_color_icon(brush.color), brush.color.to_hex())
            fitem.setEditable(False)
            self.appendRow(fitem)
        else:
            raise Exception("Unsupport brush")

    def clear_items(self) -> None:
        self.removeRows(0, self.rowCount())
