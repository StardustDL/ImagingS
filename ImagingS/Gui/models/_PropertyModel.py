from enum import Enum
from typing import Any, Dict, List

import qtawesome as qta
from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QIcon

from ImagingS import Color
from ImagingS.Gui import icons
from ImagingS.serialization import getProperties


class PropertyModel(QStandardItemModel):
    NAME, VALUE = range(2)

    def __init__(self, parent) -> None:
        super().__init__(0, 2, parent)
        self.setHeaderData(PropertyModel.NAME, Qt.Horizontal, "Name")
        self.setHeaderData(PropertyModel.VALUE, Qt.Horizontal, "Value")
        self.obj = None

    def fresh(self, obj: Any = None) -> None:
        self.removeRows(0, self.rowCount())
        self.obj = obj
        if obj is None:
            return
        name = obj.__class__.__name__
        item = QStandardItem(name)
        self._setIcon(item, name, obj)
        self._setUserData(item, obj)
        self.appendRow(item)
        self._addPropChildren(item, obj)

    def getUserData(self, index: QModelIndex) -> Any:
        item = self.itemFromIndex(index)
        return item.data(Qt.UserRole)

    def _setUserData(self, item: QStandardItem, value: Any) -> None:
        item.setData(value, Qt.UserRole)

    def _setIcon(self, item: QStandardItem, name: str, value: Any) -> None:
        if hasattr(icons, name):
            icon = getattr(icons, name)
            if isinstance(icon, QIcon):
                item.setIcon(icon)
                return
        typeName = value.__class__.__name__
        typeName = typeName[0].lower() + typeName[1:]
        if hasattr(icons, typeName):
            icon = getattr(icons, typeName)
            item.setIcon(icon)
            return
        if name == "vertexes" or name == "controlPoints":
            item.setIcon(icons.vertex)
        elif name == "brushes":
            item.setIcon(icons.brush)
        elif name == "drawings":
            item.setIcon(icons.drawing)
        elif name == "algorithm":
            item.setIcon(qta.icon("mdi.lightbulb"))
        elif isinstance(value, Color):
            item.setIcon(icons.getColorIcon(value))

    def _addDictChildren(self, root: QStandardItem, li: Dict) -> None:
        for k, v in li.items():
            self._addChild(root, str(k), v)

    def _addListChildren(self, root: QStandardItem, li: List) -> None:
        for i, value in enumerate(li):
            self._addChild(root, str(i), value)

    def _addPropChildren(self, root: QStandardItem, obj: Any) -> bool:  # return has child
        flag = False
        for prop in getProperties(obj):
            flag = True
            self._addChild(root, prop.name, prop.get())
        return flag

    def _addChild(self, root: QStandardItem, name: str, value: Any) -> None:
        item = QStandardItem(name)
        self._setIcon(item, name, value)
        self._setUserData(item, value)
        root.appendRow(item)
        index = self.indexFromItem(item).row()
        if value is None or isinstance(value, str) or isinstance(value, int):
            root.setChild(index, self.VALUE, QStandardItem(str(value)))
        elif isinstance(value, float):
            root.setChild(index, self.VALUE,
                          QStandardItem(str(round(value, 2))))
        elif isinstance(value, Enum):
            root.setChild(index, self.VALUE, QStandardItem(value.name))
        elif isinstance(value, list):
            root.setChild(index, self.VALUE, QStandardItem("List"))
            self._addListChildren(item, value)
        elif isinstance(value, dict):
            root.setChild(index, self.VALUE, QStandardItem("Dictionary"))
            self._addDictChildren(item, value)
        elif isinstance(value, set):
            root.setChild(index, self.VALUE, QStandardItem("Set"))
            self._addListChildren(item, list(value))
        else:
            if self._addPropChildren(item, value):
                root.setChild(index, self.VALUE, QStandardItem(
                    value.__class__.__name__))
            else:
                root.setChild(index, self.VALUE, QStandardItem(str(value)))
