from ImagingS.document import Document
from ImagingS.core import Color, Size, Point, RectArea
from ImagingS.core.brush import Brush, SolidBrush
from ImagingS.core.drawing import Drawing
from ImagingS.core.geometry import Line, Curve, Polygon, Ellipse
from ImagingS.core.transform import Transform, TranslateTransform, SkewTransform, RotateTransform, TransformGroup, ScaleTransform, MatrixTransform, ClipTransform
from typing import Dict, List
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from ImagingS.core.serialization import get_properties
from ._BrushModel import get_color_icon
import qtawesome as qta


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
        if isinstance(value, Color):
            item.setIcon(get_color_icon(value))
        elif isinstance(value, Document):
            item.setIcon(qta.icon("mdi.file-document"))
        elif isinstance(value, Size):
            item.setIcon(qta.icon("mdi.format-size"))
        elif isinstance(value, RectArea):
            item.setIcon(qta.icon("mdi.rectangle-outline"))
        elif isinstance(value, Point):
            item.setIcon(qta.icon("mdi.circle-medium"))
        elif isinstance(value, TranslateTransform):
            item.setIcon(qta.icon("mdi.cursor-move"))
        elif isinstance(value, SkewTransform):
            item.setIcon(qta.icon("mdi.skew-more"))
        elif isinstance(value, RotateTransform):
            item.setIcon(qta.icon("mdi.rotate-left"))
        elif isinstance(value, ScaleTransform):
            item.setIcon(qta.icon("mdi.relative-scale"))
        elif isinstance(value, MatrixTransform):
            item.setIcon(qta.icon("mdi.matrix"))
        elif isinstance(value, ClipTransform):
            item.setIcon(qta.icon("mdi.crop"))
        elif isinstance(value, TransformGroup):
            item.setIcon(qta.icon("mdi.group"))
        elif isinstance(value, SolidBrush):
            item.setIcon(qta.icon("mdi.solid"))
        elif isinstance(value, Line):
            item.setIcon(qta.icon("mdi.vector-line"))
        elif isinstance(value, Curve):
            item.setIcon(qta.icon("mdi.vector-curve"))
        elif isinstance(value, Ellipse):
            item.setIcon(qta.icon("mdi.vector-ellipse"))
        elif isinstance(value, Polygon):
            item.setIcon(qta.icon("mdi.vector-polygon"))
        elif isinstance(value, Brush) or name == "stroke" or name == "fill":
            item.setIcon(qta.icon("mdi.brush"))
        elif isinstance(value, Drawing):
            item.setIcon(qta.icon("mdi.drawing"))
        elif isinstance(value, Transform) or name == "transform":
            item.setIcon(qta.icon("mdi.axis"))
        elif name == "vertexes" or name == "control_points":
            item.setIcon(qta.icon("mdi.vector-point"))
        elif name == "x":
            item.setIcon(qta.icon("mdi.axis-x-arrow"))
        elif name == "y":
            item.setIcon(qta.icon("mdi.axis-y-arrow"))
        elif name == "id":
            item.setIcon(qta.icon("mdi.identifier"))
        elif name.startswith("angle"):
            item.setIcon(qta.icon("mdi.angle-acute"))
        elif name == "matrix":
            item.setIcon(qta.icon("mdi.matrix"))
        elif isinstance(value, list):
            item.setIcon(qta.icon("mdi.format-list-numbered"))
        elif isinstance(value, dict):
            item.setIcon(qta.icon("mdi.dictionary"))
        elif isinstance(value, set):
            item.setIcon(qta.icon("mdi.code-braces"))

    def __add_dict_children(self, root: QStandardItem, li: Dict) -> None:
        for k, v in li.items():
            self.__add_child(root, str(k), v)

    def __add_list_children(self, root: QStandardItem, li: List) -> None:
        for i, value in enumerate(li):
            self.__add_child(root, str(i), value)

    def __add_prop_children(self, root: QStandardItem, obj) -> None:
        for prop in get_properties(obj):
            self.__add_child(root, prop.name, prop.get())

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
            root.setChild(index, self.VALUE, QStandardItem(
                value.__class__.__name__))
            self.__add_prop_children(item, value)
