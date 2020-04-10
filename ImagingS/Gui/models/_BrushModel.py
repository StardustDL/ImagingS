from typing import Any

from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel

from ImagingS import Color
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
            fitem = QStandardItem()
            self._setUserData(fitem, brush)
        if fitem:
            self.appendRow(fitem)
        else:
            raise Exception("Unsupport brush")

    def data(self, index: QModelIndex, role: int) -> Any:
        brush = self.getUserData(index)
        if role == Qt.DisplayRole or role == Qt.EditRole:
            if isinstance(brush, SolidBrush):
                return brush.color.toHex()
        elif role == Qt.DecorationRole:
            if isinstance(brush, SolidBrush):
                return icons.getBrushIcon(brush)
        return super().data(index, role)

    def setData(self, index: QModelIndex, value: Any, role: int) -> bool:
        if role == Qt.EditRole:
            brush = self.getUserData(index)
            try:
                if isinstance(brush, SolidBrush):
                    brush.color = Color.fromHex(str(value))
            except Exception:
                return False
            self.dataChanged.emit(index, index, [role])
            return True
        return super().setData(index, value, role)

    def getUserData(self, index: QModelIndex) -> Brush:
        item = self.itemFromIndex(index)
        return item.data(Qt.UserRole)

    def _setUserData(self, item: QStandardItem, value: Brush) -> None:
        item.setData(value, Qt.UserRole)

    def clear_items(self) -> None:
        self.removeRows(0, self.rowCount())
