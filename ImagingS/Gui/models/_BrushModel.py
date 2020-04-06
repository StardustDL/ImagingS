import qtawesome as qta
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel

from ImagingS.core import Color
from ImagingS.core.brush import Brush, SolidBrush
from ImagingS.Gui.graphics import converters


def get_color_icon(color: Color) -> QIcon:
    # pixmap = QPixmap(32, 32)
    # pixmap.fill(converters.convert_color(color))
    # return QIcon(pixmap)
    return qta.icon("mdi.invert-colors", color=converters.convert_color(color))


def get_brush_icon(color: Color) -> QIcon:
    # pixmap = QPixmap(32, 32)
    # pixmap.fill(converters.convert_color(color))
    # return QIcon(pixmap)
    return qta.icon("mdi.brush", color=converters.convert_color(color))


class BrushModel(QStandardItemModel):
    NAME = 0

    def __init__(self, parent) -> None:
        super().__init__(0, 1, parent)
        self.setHeaderData(BrushModel.NAME, Qt.Horizontal, "Name")

    def append(self, brush: Brush) -> None:
        fitem = None
        if isinstance(brush, SolidBrush):
            fitem = QStandardItem(get_brush_icon(
                brush.color), brush.color.to_hex())

        if fitem:
            fitem.setEditable(False)
            self.appendRow(fitem)
        else:
            raise Exception("Unsupport brush")

    def clear_items(self) -> None:
        self.removeRows(0, self.rowCount())
