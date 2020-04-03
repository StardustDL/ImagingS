from ImagingS.core import Colors
from ImagingS.Gui.graphics import converters
from ImagingS.core.drawing import Drawing
from ImagingS.core.brush import SolidBrush
from ImagingS.core.geometry import Line, Polygon, Curve, Ellipse, Geometry
import qtawesome as qta
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class DrawingModel(QStandardItemModel):
    NAME = 0

    def __init__(self, parent) -> None:
        super().__init__(0, 1, parent)
        self.setHeaderData(DrawingModel.NAME, Qt.Horizontal, "Name")

    def append(self, drawing: Drawing) -> None:
        fitem = None
        if isinstance(drawing, Geometry):
            if isinstance(drawing.stroke, SolidBrush):
                color = converters.convert_color(drawing.stroke.color)
            else:
                color = converters.convert_color(Colors.Black())
            if isinstance(drawing, Line):
                fitem = QStandardItem(qta.icon("mdi.vector-line", color=color), drawing.id)
            elif isinstance(drawing, Curve):
                fitem = QStandardItem(qta.icon("mdi.vector-curve", color=color), drawing.id)
            elif isinstance(drawing, Ellipse):
                fitem = QStandardItem(
                    qta.icon("mdi.vector-ellipse", color=color), drawing.id)
            elif isinstance(drawing, Polygon):
                fitem = QStandardItem(
                    qta.icon("mdi.vector-polygon", color=color), drawing.id)

        if fitem:
            fitem.setEditable(False)
            self.appendRow(fitem)
        else:
            raise Exception("Unsupport drawing")

    def clear_items(self) -> None:
        self.removeRows(0, self.rowCount())
