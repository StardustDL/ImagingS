from enum import Enum
from typing import Any, Dict, List

import qtawesome as qta
from PyQt5.QtCore import QModelIndex, Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel

from ImagingS import Color
from ImagingS.Gui import icons
from ImagingS.serialization import Property, getProperties


class PropertyModel(QStandardItemModel):
    NAME, VALUE = range(2)
    changed = pyqtSignal()

    def __init__(self, parent) -> None:
        super().__init__(0, 2, parent)
        self.setHeaderData(PropertyModel.NAME, Qt.Horizontal, "Name")
        self.setHeaderData(PropertyModel.VALUE, Qt.Horizontal, "Value")
        self.onlyEditable = False
        self.obj = None

    def fresh(self, obj: Any = None) -> None:
        self.removeRows(0, self.rowCount())
        self.obj = obj
        if obj is None:
            return
        name = obj.__class__.__name__
        item = QStandardItem(name)
        item.setEditable(False)
        self._setIcon(item, name, obj)
        self._setUserData(item, obj)
        self.appendRow(item)
        self._addPropChildren(item, obj)

    @property
    def onlyEditable(self) -> bool:
        return self._onlyEditable

    @onlyEditable.setter
    def onlyEditable(self, value: bool) -> None:
        self._onlyEditable = value

    def data(self, index: QModelIndex, role: int) -> Any:
        if index.column() == self.VALUE:
            value = self.getUserData(index)
            if isinstance(value, Property):
                realValue = value.get()
                if role == Qt.DisplayRole or role == Qt.EditRole:
                    if realValue is None:
                        return "None"
                    elif isinstance(realValue, str):
                        return realValue
                    elif isinstance(realValue, int):
                        return str(realValue)
                    elif isinstance(realValue, float):
                        return str(round(realValue, 2))
                    elif isinstance(realValue, Enum):
                        return realValue.name
        return super().data(index, role)

    def setData(self, index: QModelIndex, value: Any, role: int) -> bool:
        if index.column() == self.VALUE:
            data = self.getUserData(index)
            if isinstance(data, Property):
                realData = data.get()
                if role == Qt.DisplayRole or role == Qt.EditRole:
                    modified = True
                    if isinstance(realData, str):
                        try:
                            data.set(str(value))
                        except Exception:
                            return False
                    elif isinstance(realData, int):
                        try:
                            data.set(int(value))
                        except Exception:
                            return False
                    elif isinstance(realData, float):
                        try:
                            data.set(float(value))
                        except Exception:
                            return False
                    elif isinstance(realData, Enum):
                        try:
                            en = getattr(realData.__class__, value)
                            assert isinstance(en, realData.__class__)
                            data.set(en)
                        except Exception:
                            return False
                    else:
                        modified = False
                    if modified:
                        self.dataChanged.emit(index, index, [role])
                        self.changed.emit()
                        return True
        return super().setData(index, value, role)

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
            if self.onlyEditable and not prop.canSet:
                continue
            flag = True
            self._addChild(root, prop.name, prop)
        return flag

    def _addChild(self, root: QStandardItem, name: str, value: Any) -> None:
        item = QStandardItem(name)
        item.setEditable(False)
        self._setUserData(item, value)
        valueItem = QStandardItem()
        self._setUserData(valueItem, value)

        realValue = value
        if isinstance(value, Property):
            realValue = value.get()
            valueItem.setEditable(value.canSet)

        self._setIcon(item, name, realValue)
        root.appendRow(item)
        index = self.indexFromItem(item).row()
        if realValue is None or isinstance(realValue, int) or isinstance(realValue, float) or isinstance(realValue, str):
            pass
        elif isinstance(realValue, list):
            valueItem.setText("List")
            valueItem.setEditable(False)
            self._addListChildren(item, realValue)
        elif isinstance(realValue, dict):
            valueItem.setText("Dictionary")
            valueItem.setEditable(False)
            self._addDictChildren(item, realValue)
        elif isinstance(realValue, set):
            valueItem.setText("Set")
            valueItem.setEditable(False)
            self._addListChildren(item, list(realValue))
        else:
            if self._addPropChildren(item, realValue):
                valueItem.setText(realValue.__class__.__name__)
                valueItem.setEditable(False)
            else:
                valueItem.setText(str(realValue))
                valueItem.setEditable(False)
        if name == "id":
            valueItem.setEditable(False)
        root.setChild(index, self.VALUE, valueItem)
