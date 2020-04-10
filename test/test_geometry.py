from ImagingS import Point, Rect, Size
from ImagingS.drawing import Pen
from ImagingS.geometry import (CurveAlgorithm, CurveGeometry, EllipseGeometry,
                               GeometryGroup, LineAlgorithm, LineGeometry,
                               PolygonGeometry, PolylineGeometry,
                               RectangleGeometry)


def test_line() -> None:
    line = LineGeometry(Point(
        0, 0), Point(1, 1), LineAlgorithm.Dda)
    assert line.inStroke(Pen(), Point())
    assert not line.inFill(Point())
    line = LineGeometry(Point(
        0, 0), Point(1, 1), LineAlgorithm.Bresenham)
    assert line.inStroke(Pen(), Point())
    assert not line.inFill(Point())


def test_poly() -> None:
    vertex = [Point(0, 0), Point(
        1, 0), Point(1, 1), Point(0.5, 0.5)]
    line = PolylineGeometry(vertex, LineAlgorithm.Dda)
    assert line.inStroke(Pen(), Point())
    assert not line.inFill(Point())
    line = PolygonGeometry(vertex, LineAlgorithm.Dda)
    assert line.inStroke(Pen(), Point())
    assert not line.inFill(Point())
    line = RectangleGeometry(
        Rect(Point(), Size(10, 10)), LineAlgorithm.Dda)
    assert line.inStroke(Pen(), Point())
    assert not line.inFill(Point())


def test_curve() -> None:
    control = [Point(0, 0), Point(
        1, 0), Point(1, 1), Point(0.5, 0.5)]
    curve = CurveGeometry(control, CurveAlgorithm.Bezier)
    assert curve.inStroke(Pen(), Point())
    curve = CurveGeometry(control, CurveAlgorithm.BSpline)
    assert not curve.inStroke(Pen(), Point())


def test_ellipse() -> None:
    ell = EllipseGeometry.fromRect(
        Rect(Point(), Size(10, 10)))
    assert not ell.inStroke(Pen(), Point())


def test_group() -> None:
    line = LineGeometry(Point(
        0, 0), Point(1, 1), LineAlgorithm.Dda)
    ell = EllipseGeometry.fromRect(
        Rect(Point(), Size(10, 10)))
    group = GeometryGroup()
    group.children.append(line)
    group.children.append(ell)
    list(group.strokePoints(Pen()))
    list(group.fillPoints())
    assert group.inStroke(Pen(), Point())
    assert not group.inFill(Point())
