from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel

from ImagingS.brush import Brush, SolidBrush
from ImagingS.Gui import icons


class BrushModel(QStandardItemModel):
    NAME = 0

    def __init__(self, parent) -> None:
        super().__init__(0, 1, parent)
        self.setHeaderData(BrushModel.NAME, Qt.Horizontal, "Name")

    def append(self, brush: Brush) -> None:
        fitem = None
        if isinstance(brush, SolidBrush):
            fitem = QStandardItem(icons.get_brush_icon(
                brush), brush.color.to_hex())

        if fitem:
            fitem.setEditable(False)
            self.appendRow(fitem)
        else:
            raise Exception("Unsupport brush")

    def clear_items(self) -> None:
        self.removeRows(0, self.rowCount())
