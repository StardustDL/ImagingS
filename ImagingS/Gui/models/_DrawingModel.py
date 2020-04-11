from typing import Any

from PyQt5.QtCore import QModelIndex, Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel

from ImagingS.drawing import Drawing, DrawingGroup, GeometryDrawing
from ImagingS.geometry import (CurveGeometry, EllipseGeometry, LineGeometry,
                               PolygonGeometry, PolylineGeometry,
                               RectangleGeometry)
from ImagingS.Gui import icons


class DrawingModel(QStandardItemModel):
    ID, TYPE = range(2)
    changed = pyqtSignal()

    def __init__(self, parent) -> None:
        super().__init__(0, 1, parent)
        self.setHeaderData(DrawingModel.ID, Qt.Horizontal, "Id")
        self.setHeaderData(DrawingModel.TYPE, Qt.Horizontal, "Type")
        self.obj = None

    def fresh(self, obj: Drawing = None) -> None:
        self.removeRows(0, self.rowCount())
        self.obj = obj
        if obj is None:
            return

        type = obj.__class__.__name__
        item = QStandardItem()
        item.setEditable(False)
        index = self.indexFromItem(item).row()
        typeItem = QStandardItem(type)
        typeItem.setEditable(False)
        self.setItem(index, self.TYPE, typeItem)
        self._setUserData(item, obj)
        self.appendRow(item)

        if isinstance(obj, DrawingGroup):
            self._addChildren(item, obj)

    def data(self, index: QModelIndex, role: int) -> Any:
        if index.column() == self.ID:
            drawing = self.getUserData(index)
            if role == Qt.DisplayRole or role == Qt.EditRole:
                if drawing == self.obj:  # Root
                    return "Document"
                else:
                    return drawing.id
            elif role == Qt.DecorationRole:
                return self._getIcon(drawing)
        return super().data(index, role)

    def setData(self, index: QModelIndex, value: Any, role: int) -> bool:
        if role == Qt.EditRole:
            if index.column() == self.ID:
                drawing = self.getUserData(index)
                try:
                    parent = drawing.parent()
                    if parent is not None:
                        parent.setItemId(drawing.id, str(value))
                    else:
                        drawing.id = str(value)
                except Exception:
                    return False
                self.dataChanged.emit(index, index, [role])
                self.changed.emit()
                return True
        return super().setData(index, value, role)

    def getUserData(self, index: QModelIndex) -> Drawing:
        item = self.itemFromIndex(index)
        return item.data(Qt.UserRole)

    def _setUserData(self, item: QStandardItem, value: Drawing) -> None:
        item.setData(value, Qt.UserRole)

    def _getIcon(self, value: Drawing) -> QIcon:
        if isinstance(value, GeometryDrawing):
            if isinstance(value.geometry, LineGeometry):
                return icons.lineGeometry
            elif isinstance(value.geometry, CurveGeometry):
                return icons.curveGeometry
            elif isinstance(value.geometry, EllipseGeometry):
                return icons.ellipseGeometry
            elif isinstance(value.geometry, RectangleGeometry):
                return icons.rectangleGeometry
            elif isinstance(value.geometry, PolygonGeometry):
                return icons.polygonGeometry
            elif isinstance(value.geometry, PolylineGeometry):
                return icons.polylineGeometry
        return icons.drawing

    def _addChildren(self, root: QStandardItem, value: DrawingGroup) -> None:
        for drawing in value.children:
            type = drawing.__class__.__name__
            item = QStandardItem(drawing.id)
            self._setUserData(item, drawing)
            root.appendRow(item)
            index = self.indexFromItem(item).row()

            typeItem = QStandardItem(type)
            typeItem.setEditable(False)
            root.setChild(index, self.TYPE, typeItem)

            if isinstance(drawing, DrawingGroup):
                self._addChildren(item, drawing)
