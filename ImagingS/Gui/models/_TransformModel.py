from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QStandardItem, QStandardItemModel

from ImagingS.Gui import icons
from ImagingS.transform import (MatrixTransform, RotateTransform,
                                ScaleTransform, SkewTransform, Transform,
                                TransformGroup, TranslateTransform)


class TransformModel(QStandardItemModel):
    TYPE = range(1)

    def __init__(self, parent) -> None:
        super().__init__(0, 1, parent)
        self.setHeaderData(TransformModel.TYPE, Qt.Horizontal, "Type")
        self.obj = None

    def fresh(self, obj: Transform = None) -> None:
        self.removeRows(0, self.rowCount())
        self.obj = obj
        if obj is None:
            return

        name = obj.__class__.__name__
        item = QStandardItem(name)
        self.__set_icon(item, obj)
        self.__set_data(item, obj)
        self.appendRow(item)

        if isinstance(obj, TransformGroup):
            self.__add_children(item, obj)

    def get_data(self, index: QModelIndex) -> Transform:
        item = self.itemFromIndex(index)
        return item.data(Qt.UserRole)

    def __set_data(self, item: QStandardItem, value: Transform) -> None:
        item.setData(value, Qt.UserRole)

    def __set_icon(self, item: QStandardItem, value: Transform) -> None:
        if isinstance(value, TranslateTransform):
            item.setIcon(icons.translateTransform)
        elif isinstance(value, SkewTransform):
            item.setIcon(icons.skewTransform)
        elif isinstance(value, RotateTransform):
            item.setIcon(icons.rotateTransform)
        elif isinstance(value, ScaleTransform):
            item.setIcon(icons.scaleTransform)
        elif isinstance(value, MatrixTransform):
            item.setIcon(icons.matrixTransform)
        elif isinstance(value, TransformGroup):
            item.setIcon(icons.groupTransform)

    def __add_children(self, root: QStandardItem, value: TransformGroup) -> None:
        for trans in value.children:
            name = trans.__class__.__name__
            item = QStandardItem(name)
            self.__set_icon(item, trans)
            self.__set_data(item, trans)
            root.appendRow(item)
            if isinstance(trans, TransformGroup):
                self.__add_children(item, trans)
