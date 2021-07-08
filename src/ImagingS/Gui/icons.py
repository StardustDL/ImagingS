import qtawesome as qta
from PyQt5.QtGui import QIcon

from ImagingS import Color
from ImagingS.brush import SolidBrush

from . import converters

grid: QIcon = qta.icon("mdi.grid")

refresh: QIcon = qta.icon("mdi.refresh")

list: QIcon = qta.icon("mdi.format-list-numbered")

set: QIcon = qta.icon("mdi.code-braces")

code: QIcon = qta.icon("mdi.code-tags")

fileTree: QIcon = qta.icon("mdi.file-tree")

visual: QIcon = qta.icon("mdi.image")

vertex: QIcon = qta.icon("mdi.vector-point")

stroke: QIcon = qta.icon("mdi.border-color")

fill: QIcon = qta.icon("mdi.format-color-fill")

x: QIcon = qta.icon("mdi.axis-x-arrow")

y: QIcon = qta.icon("mdi.axis-y-arrow")

r: QIcon = qta.icon("mdi.alpha-r-circle", color="red")

g: QIcon = qta.icon("mdi.alpha-g-circle", color="green")

b: QIcon = qta.icon("mdi.alpha-b-circle", color="blue")

width: QIcon = qta.icon("mdi.alpha-w-circle")

height: QIcon = qta.icon("mdi.alpha-h-circle")

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

lineGeometry: QIcon = qta.icon("mdi.vector-line")

curveGeometry: QIcon = qta.icon("mdi.vector-curve")

ellipseGeometry: QIcon = qta.icon("mdi.vector-ellipse")

polygonGeometry: QIcon = qta.icon("mdi.vector-polygon")

polylineGeometry: QIcon = qta.icon("mdi.vector-polyline")

rectangleGeometry: QIcon = qta.icon("mdi.vector-rectangle")

clip: QIcon = qta.icon("mdi.crop")

skewTransform: QIcon = qta.icon("mdi.skew-more")

scaleTransform: QIcon = qta.icon("mdi.relative-scale")

translateTransform: QIcon = qta.icon("mdi.cursor-move")

rotateTransform: QIcon = qta.icon("mdi.rotate-left")

matrixTransform: QIcon = matrix

transformGroup: QIcon = qta.icon("mdi.group")


def getColorIcon(color: Color) -> QIcon:
    return qta.icon("mdi.invert-colors", color=converters.qcolor(color))


def getBrushIcon(brush: SolidBrush) -> QIcon:
    # pixmap = QPixmap(32, 32)
    # pixmap.fill(converters.convert_color(color))
    # return QIcon(pixmap)
    return qta.icon("mdi.brush", color=converters.qcolor(brush.color))
