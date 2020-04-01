from typing import Iterator
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class Property:
    def __init__(self, name: str, onwer, prop: property):
        self.name = name
        self.onwer = onwer
        self._get = prop.fget
        self._set = prop.fset
        self._del = prop.fdel

    def can_get(self):
        return self._get is not None

    def can_set(self):
        return self._set is not None

    def can_del(self):
        return self._del is not None

    def get(self):
        return self._get.__call__(self.onwer)

    def set(self, val):
        return self._set.__call__(self.onwer, val)

    def delete(self):
        return self._del.__call__(self.onwer)


def _get_props(obj) -> Iterator[Property]:
    cls = obj.__class__
    for name in dir(cls):
        item = getattr(cls, name)
        if isinstance(item, property):
            yield Property(name, obj, item)


class PropertyModel(QStandardItemModel):
    NAME, VALUE = range(2)

    def __init__(self, parent) -> None:
        super().__init__(0, 2, parent)
        self.setHeaderData(PropertyModel.NAME, Qt.Horizontal, "Name")
        self.setHeaderData(PropertyModel.VALUE, Qt.Horizontal, "Value")
        self.obj = None

    def fresh(self, obj=None) -> None:
        self.removeRows(0, self.rowCount())
        self.obj = obj
        if obj is None:
            return
        for prop in _get_props(obj):
            index = self.rowCount()
            item = QStandardItem(prop.name)
            self.appendRow(item)
            self.setData(self.index(index, self.VALUE), prop.get())
