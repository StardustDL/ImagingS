from typing import Union

from PyQt5.QtCore import QPoint, QPointF, QRect, QRectF, QSize, QSizeF
from PyQt5.QtGui import QColor

from ImagingS import Color, Point, Rect, Size


def qpoint(o: Point) -> QPointF:
    return QPointF(o.x, o.y)


def qsize(o: Size) -> QSizeF:
    return QSizeF(o.width, o.height)


def qrect(o: Rect) -> QRectF:
    return QRectF(qpoint(o.origin), qsize(o.size))


def qcolor(o: Color) -> QColor:
    return QColor(o.r, o.g, o.b)


def point(o: Union[QPointF, QPoint]) -> Point:
    return Point.create(o.x(), o.y())


def size(o: Union[QSizeF, QSize]) -> Size:
    return Size.create(o.width(), o.height())


def rect(o: Union[QRectF, QRect]) -> Rect:
    return Rect.create(qpoint(o.topLeft()), qsize(o.size()))


def color(o: QColor) -> Color:
    return Color.create(o.red(), o.green(), o.blue())
