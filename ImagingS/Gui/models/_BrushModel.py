from ImagingS.core import Color
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QIcon, QPixmap, QColor, QStandardItem
from ImagingS.core.brush import Brush, Solid


def _get_color_icon(color: Color) -> QIcon:
    pixmap = QPixmap(32, 32)
    pixmap.fill(QColor(color.r, color.g, color.b))
    return QIcon(pixmap)


class BrushModel(QStandardItemModel):
    NAME, VALUE = range(2)

    def __init__(self, parent) -> None:
        super().__init__(0, 2, parent)
        self.setHeaderData(BrushModel.NAME, Qt.Horizontal, "Name")
        self.setHeaderData(BrushModel.VALUE, Qt.Horizontal, "Value")

    def append(self, brush: Brush) -> None:
        index = self.rowCount()
        if isinstance(brush, Solid):
            self.appendRow(QStandardItem(_get_color_icon(brush.color), brush.id))
            self.setData(self.index(index, self.VALUE), brush.color.to_hex())
        else:
            raise Exception("Unsupport brush")

    def clear_items(self) -> None:
        self.removeRows(0, self.rowCount())
