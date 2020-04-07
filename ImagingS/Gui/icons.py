import qtawesome as qta
from PyQt5.QtGui import QIcon

from ImagingS.core import Color
from ImagingS.core.brush import SolidBrush

from . import converters

list: QIcon = qta.icon("mdi.format-list-numbered")

set: QIcon = qta.icon("mdi.code-braces")

dictionary: QIcon = qta.icon("mdi.dictionary")

vertex: QIcon = qta.icon("mdi.vector-point")

stroke: QIcon = qta.icon("mdi.border-color")

fill: QIcon = qta.icon("mdi.format-color-fill")

x: QIcon = qta.icon("mdi.axis-x-arrow")

y: QIcon = qta.icon("mdi.axis-y-arrow")

id: QIcon = qta.icon("mdi.identifier")

angle: QIcon = qta.icon("mdi.angle-acute")

matrix: QIcon = qta.icon("mdi.matrix")

center: QIcon = qta.icon("mdi.image-filter-center-focus")

document: QIcon = qta.icon("mdi.file-document")

size: QIcon = qta.icon("mdi.format-size")

rect: QIcon = qta.icon("mdi.rectangle-outline")

point: QIcon = qta.icon("mdi.circle-medium")

drawing: QIcon = qta.icon("mdi.drawing-box")

geometry: QIcon = qta.icon("mdi.drawing")

brush: QIcon = qta.icon("mdi.brush")

solidBrush: QIcon = qta.icon("mdi.solid")

property: QIcon = qta.icon("mdi.database")

transform: QIcon = qta.icon("mdi.flash")

line: QIcon = qta.icon("mdi.vector-line")

curve: QIcon = qta.icon("mdi.vector-curve")

ellipse: QIcon = qta.icon("mdi.vector-ellipse")

polygon: QIcon = qta.icon("mdi.vector-polygon")

clip: QIcon = qta.icon("mdi.crop")

skewTransform: QIcon = qta.icon("mdi.skew-more")

scaleTransform: QIcon = qta.icon("mdi.relative-scale")

translateTransform: QIcon = qta.icon("mdi.cursor-move")

rotateTransform: QIcon = qta.icon("mdi.rotate-left")

matrixTransform: QIcon = matrix

groupTransform: QIcon = qta.icon("mdi.group")


def get_color_icon(color: Color) -> QIcon:
    return qta.icon("mdi.invert-colors", color=converters.convert_color(color))


def get_brush_icon(brush: SolidBrush) -> QIcon:
    # pixmap = QPixmap(32, 32)
    # pixmap.fill(converters.convert_color(color))
    # return QIcon(pixmap)
    return qta.icon("mdi.brush", color=converters.convert_color(brush.color))
