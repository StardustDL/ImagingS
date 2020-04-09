from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel

from ImagingS.brush import Brush, SolidBrush
from ImagingS.Gui import icons


class BrushModel(QStandardItemModel):
    VALUE = 0

    def __init__(self, parent) -> None:
        super().__init__(0, 1, parent)
        self.setHeaderData(BrushModel.VALUE, Qt.Horizontal, "Value")

    def append(self, brush: Brush) -> None:
        fitem = None
        if isinstance(brush, SolidBrush):
            fitem = QStandardItem(icons.getBrushIcon(
                brush), brush.color.toHex())
            self._setData(fitem, brush)

        if fitem:
            self.appendRow(fitem)
        else:
            raise Exception("Unsupport brush")

    def getData(self, index: QModelIndex) -> Brush:
        item = self.itemFromIndex(index)
        return item.data(Qt.UserRole)

    def _setData(self, item: QStandardItem, value: Brush) -> None:
        item.setData(value, Qt.UserRole)

    def clear_items(self) -> None:
        self.removeRows(0, self.rowCount())
