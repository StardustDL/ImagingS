from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel

from ImagingS.drawing import Drawing, DrawingGroup, GeometryDrawing
from ImagingS.geometry import (CurveGeometry, EllipseGeometry, LineGeometry,
                               PolygonGeometry)
from ImagingS.Gui import icons


class DrawingModel(QStandardItemModel):
    ID, TYPE = range(2)

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
        item = QStandardItem(obj.id if obj.id else "Document")
        index = self.indexFromItem(item).row()
        self.setItem(index, self.TYPE, QStandardItem(type))
        self._setIcon(item, obj)
        self._setData(item, obj)
        self.appendRow(item)

        if isinstance(obj, DrawingGroup):
            self._addChildren(item, obj)

    def getData(self, index: QModelIndex) -> Drawing:
        item = self.itemFromIndex(index)
        return item.data(Qt.UserRole)

    def _setData(self, item: QStandardItem, value: Drawing) -> None:
        item.setData(value, Qt.UserRole)

    def _setIcon(self, item: QStandardItem, value: Drawing) -> None:
        if isinstance(value, GeometryDrawing):
            if isinstance(value.geometry, LineGeometry):
                item.setIcon(icons.lineGeometry)
            elif isinstance(value.geometry, CurveGeometry):
                item.setIcon(icons.curveGeometry)
            elif isinstance(value.geometry, EllipseGeometry):
                item.setIcon(icons.ellipseGeometry)
            elif isinstance(value.geometry, PolygonGeometry):
                item.setIcon(icons.polygonGeometry)
        else:
            item.setIcon(icons.drawing)

    def _addChildren(self, root: QStandardItem, value: DrawingGroup) -> None:
        for drawing in value.children:
            type = drawing.__class__.__name__
            item = QStandardItem(drawing.id)
            self._setIcon(item, drawing)
            self._setData(item, drawing)
            root.appendRow(item)
            index = self.indexFromItem(item).row()
            root.setChild(index, self.TYPE, QStandardItem(type))
            if isinstance(drawing, DrawingGroup):
                self._addChildren(item, drawing)
