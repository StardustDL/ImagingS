import qtawesome as qta
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel

from ImagingS.core import Colors
from ImagingS.core.brush import SolidBrush
from ImagingS.core.drawing import Drawing, GeometryDrawing
from ImagingS.core.geometry import (CurveGeometry, EllipseGeometry,
                                    LineGeometry, PolygonGeometry)
from ImagingS.Gui import converters


class DrawingModel(QStandardItemModel):
    NAME = 0

    def __init__(self, parent) -> None:
        super().__init__(0, 1, parent)
        self.setHeaderData(DrawingModel.NAME, Qt.Horizontal, "Name")

    def append(self, drawing: Drawing) -> None:
        fitem = None
        if isinstance(drawing, GeometryDrawing):
            if isinstance(drawing.stroke.brush, SolidBrush):
                color = converters.convert_color(drawing.stroke.brush.color)
            else:
                color = converters.convert_color(Colors.Black())
            if isinstance(drawing.geometry, LineGeometry):
                fitem = QStandardItem(
                    qta.icon("mdi.vector-line", color=color), drawing.id)
            elif isinstance(drawing.geometry, CurveGeometry):
                fitem = QStandardItem(
                    qta.icon("mdi.vector-curve", color=color), drawing.id)
            elif isinstance(drawing.geometry, EllipseGeometry):
                fitem = QStandardItem(
                    qta.icon("mdi.vector-ellipse", color=color), drawing.id)
            elif isinstance(drawing.geometry, PolygonGeometry):
                fitem = QStandardItem(
                    qta.icon("mdi.vector-polygon", color=color), drawing.id)

        if fitem:
            fitem.setEditable(False)
            self.appendRow(fitem)
        else:
            raise Exception("Unsupport drawing")

    def clear_items(self) -> None:
        self.removeRows(0, self.rowCount())
