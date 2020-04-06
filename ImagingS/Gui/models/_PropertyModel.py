from typing import Dict, List

import qtawesome as qta
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel

from ImagingS.core import Color, Point, Rect, Size
from ImagingS.core.brush import Brush, SolidBrush
from ImagingS.core.drawing import Drawing
from ImagingS.core.geometry import Geometry, CurveGeometry, EllipseGeometry, LineGeometry, PolygonGeometry
from ImagingS.core.serialization import get_properties
from ImagingS.core.transform import (MatrixTransform,
                                     RotateTransform, ScaleTransform,
                                     SkewTransform, Transform, TransformGroup,
                                     TranslateTransform)
from ImagingS.document import Document
from ImagingS.Gui import icons

from ._BrushModel import get_color_icon


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
        name = obj.__class__.__name__
        item = QStandardItem(name)
        self.__set_icon(item, name, obj)
        self.appendRow(item)
        self.__add_prop_children(item, obj)

    def __set_icon(self, item: QStandardItem, name, value) -> None:
        if name == "vertexes" or name == "control_points":
            item.setIcon(icons.vertex)
        elif name == "stroke":
            item.setIcon(icons.stroke)
        elif name == "fill":
            item.setIcon(icons.fill)
        elif name == "x":
            item.setIcon(icons.x)
        elif name == "y":
            item.setIcon(icons.y)
        elif name == "id":
            item.setIcon(icons.id)
        elif name.startswith("angle"):
            item.setIcon(icons.angle)
        elif name == "matrix":
            item.setIcon(icons.matrix)
        elif name == "r":
            item.setIcon(qta.icon("mdi.alpha-r-circle"))
        elif name == "g":
            item.setIcon(qta.icon("mdi.alpha-g-circle"))
        elif name == "b":
            item.setIcon(qta.icon("mdi.alpha-b-circle"))
        elif name == "width":
            item.setIcon(qta.icon("mdi.alpha-w-circle"))
        elif name == "height":
            item.setIcon(qta.icon("mdi.alpha-h-circle"))
        elif name == "brushes":
            item.setIcon(icons.brush)
        elif name == "drawings":
            item.setIcon(icons.drawing)
        elif name == "geometry":
            item.setIcon(icons.geometry)
        elif name == "matrix":
            item.setIcon(icons.matrix)
        elif name == "center":
            item.setIcon(icons.center)
        elif name == "algorithm":
            item.setIcon(qta.icon("mdi.lightbulb"))
        elif isinstance(value, Color):
            item.setIcon(get_color_icon(value))
        elif isinstance(value, Document):
            item.setIcon(icons.document)
        elif isinstance(value, Size):
            item.setIcon(icons.size)
        elif isinstance(value, Rect):
            item.setIcon(icons.rect)
        elif isinstance(value, Point):
            item.setIcon(icons.point)
        elif isinstance(value, TranslateTransform):
            item.setIcon(icons.translateTransform)
        elif isinstance(value, SkewTransform):
            item.setIcon(icons.skewTransform)
        elif isinstance(value, RotateTransform):
            item.setIcon(icons.rotateTransform)
        elif isinstance(value, ScaleTransform):
            item.setIcon(icons.scaleTransform)
        elif isinstance(value, MatrixTransform):
            item.setIcon(icons.matrixTransform)
        elif isinstance(value, ClipTransform):
            item.setIcon(icons.clipTransform)
        elif isinstance(value, TransformGroup):
            item.setIcon(icons.groupTransform)
        elif isinstance(value, SolidBrush):
            item.setIcon(icons.solidBrush)
        elif isinstance(value, LineGeometry):
            item.setIcon(icons.line)
        elif isinstance(value, CurveGeometry):
            item.setIcon(icons.curve)
        elif isinstance(value, EllipseGeometry):
            item.setIcon(icons.ellipse)
        elif isinstance(value, PolygonGeometry):
            item.setIcon(icons.polygon)
        elif isinstance(value, Brush):
            item.setIcon(icons.brush)
        elif isinstance(value, Drawing):
            item.setIcon(icons.drawing)
        elif isinstance(value, Geometry):
            item.setIcon(icons.geometry)
        elif isinstance(value, Transform) or name == "transform":
            item.setIcon(icons.transform)
        elif isinstance(value, list):
            item.setIcon(icons.list)
        elif isinstance(value, dict):
            item.setIcon(icons.dictionary)
        elif isinstance(value, set):
            item.setIcon(icons.set)

    def __add_dict_children(self, root: QStandardItem, li: Dict) -> None:
        for k, v in li.items():
            self.__add_child(root, str(k), v)

    def __add_list_children(self, root: QStandardItem, li: List) -> None:
        for i, value in enumerate(li):
            self.__add_child(root, str(i), value)

    def __add_prop_children(self, root: QStandardItem, obj) -> bool:  # return has child
        flag = False
        for prop in get_properties(obj):
            flag = True
            self.__add_child(root, prop.name, prop.get())
        return flag

    def __add_child(self, root: QStandardItem, name: str, value) -> None:
        item = QStandardItem(name)
        self.__set_icon(item, name, value)
        root.appendRow(item)
        index = self.indexFromItem(item).row()
        if value is None or isinstance(value, str) or isinstance(value, int) or isinstance(value, float):
            root.setChild(index, self.VALUE, QStandardItem(str(value)))
        elif isinstance(value, list):
            root.setChild(index, self.VALUE, QStandardItem("List"))
            self.__add_list_children(item, value)
        elif isinstance(value, dict):
            root.setChild(index, self.VALUE, QStandardItem("Dictionary"))
        elif isinstance(value, set):
            root.setChild(index, self.VALUE, QStandardItem("Set"))
            self.__add_list_children(item, list(value))
        else:
            if self.__add_prop_children(item, value):
                root.setChild(index, self.VALUE, QStandardItem(
                    value.__class__.__name__))
            else:
                root.setChild(index, self.VALUE, QStandardItem(str(value)))
