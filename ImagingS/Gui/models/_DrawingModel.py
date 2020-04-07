from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QStandardItem, QStandardItemModel

from ImagingS.drawing import Drawing, GeometryDrawing, DrawingGroup
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
        item = QStandardItem(obj.id)
        index = self.indexFromItem(item).row()
        self.setItem(index, self.TYPE, QStandardItem(type))
        self.__set_icon(item, obj)
        self.__set_data(item, obj)
        self.appendRow(item)

        if isinstance(obj, DrawingGroup):
            self.__add_children(item, obj)

    def get_data(self, index: QModelIndex) -> Drawing:
        item = self.itemFromIndex(index)
        return item.data(Qt.UserRole)

    def __set_data(self, item: QStandardItem, value: Drawing) -> None:
        item.setData(value, Qt.UserRole)

    def __set_icon(self, item: QStandardItem, value: Drawing) -> None:
        if isinstance(value, GeometryDrawing):
            if isinstance(value.geometry, LineGeometry):
                item.setIcon(icons.line)
            elif isinstance(value.geometry, CurveGeometry):
                item.setIcon(icons.curve)
            elif isinstance(value.geometry, EllipseGeometry):
                item.setIcon(icons.ellipse)
            elif isinstance(value.geometry, PolygonGeometry):
                item.setIcon(icons.polygon)

    def __add_children(self, root: QStandardItem, value: DrawingGroup) -> None:
        for drawing in value.children:
            type = drawing.__class__.__name__
            item = QStandardItem(drawing.id)
            index = self.indexFromItem(item).row()
            self.setItem(index, self.TYPE, QStandardItem(type))
            self.__set_icon(item, drawing)
            self.__set_data(item, drawing)
            self.appendRow(item)
            if isinstance(drawing, DrawingGroup):
                self.__add_children(item, drawing)
