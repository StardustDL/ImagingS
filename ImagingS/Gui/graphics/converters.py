from ImagingS.core import Point, Size, RectArea, Color
from PyQt5.QtCore import QPointF, QSizeF, QRectF, QPoint, QSize, QRect
from PyQt5.QtGui import QColor
from typing import Union


def convert_point(o: Point) -> QPointF:
    return QPointF(o.x, o.y)


def convert_size(o: Size) -> QSizeF:
    return QSizeF(o.width, o.height)


def convert_rect_area(o: RectArea) -> QRectF:
    return QRectF(convert_point(o.origin), convert_size(o.size))


def convert_color(o: Color) -> QColor:
    return QColor(o.r, o.g, o.b)


def convert_qpoint(o: Union[QPointF, QPoint]) -> Point:
    return Point.create(o.x(), o.y())


def convert_qsize(o: Union[QSizeF, QSize]) -> Size:
    return Size.create(o.width, o.height)


def convert_qrect_area(o: Union[QRectF, QRect]) -> RectArea:
    return RectArea.create(convert_qpoint(o.topLeft()), convert_qsize(o.size()))


def convert_qcolor(o: QColor) -> Color:
    return Color.create(o.red(), o.green(), o.blue())
