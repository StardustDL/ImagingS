from ImagingS import Point, Rect, Size
from ImagingS.drawing import Pen
from ImagingS.geometry import (CurveAlgorithm, CurveGeometry, EllipseGeometry,
                               GeometryGroup, LineAlgorithm, LineGeometry,
                               PolygonGeometry, PolylineGeometry,
                               RectangleGeometry)


def test_line() -> None:
    line = LineGeometry.create(Point.create(
        0, 0), Point.create(1, 1), LineAlgorithm.Dda)
    assert line.inStroke(Pen(), Point())
    assert not line.inFill(Point())
    line = LineGeometry.create(Point.create(
        0, 0), Point.create(1, 1), LineAlgorithm.Bresenham)
    assert line.inStroke(Pen(), Point())
    assert not line.inFill(Point())


def test_poly() -> None:
    vertex = [Point.create(0, 0), Point.create(
        1, 0), Point.create(1, 1), Point.create(0.5, 0.5)]
    line = PolylineGeometry.create(vertex, LineAlgorithm.Dda)
    assert line.inStroke(Pen(), Point())
    assert not line.inFill(Point())
    line = PolygonGeometry.create(vertex, LineAlgorithm.Dda)
    assert line.inStroke(Pen(), Point())
    assert not line.inFill(Point())
    line = RectangleGeometry.create(
        Rect.create(Point(), Size.create(10, 10)), LineAlgorithm.Dda)
    assert line.inStroke(Pen(), Point())
    assert not line.inFill(Point())


def test_curve() -> None:
    control = [Point.create(0, 0), Point.create(
        1, 0), Point.create(1, 1), Point.create(0.5, 0.5)]
    curve = CurveGeometry.create(control, CurveAlgorithm.Bezier)
    assert curve.inStroke(Pen(), Point())
    curve = CurveGeometry.create(control, CurveAlgorithm.BSpline)
    assert not curve.inStroke(Pen(), Point())


def test_ellipse() -> None:
    ell = EllipseGeometry.fromRect(
        Rect.create(Point(), Size.create(10, 10)))
    assert not ell.inStroke(Pen(), Point())


def test_group() -> None:
    line = LineGeometry.create(Point.create(
        0, 0), Point.create(1, 1), LineAlgorithm.Dda)
    ell = EllipseGeometry.fromRect(
        Rect.create(Point(), Size.create(10, 10)))
    group = GeometryGroup()
    group.children.append(line)
    group.children.append(ell)
    list(group.strokePoints(Pen()))
    list(group.fillPoints())
    assert group.inStroke(Pen(), Point())
    assert not group.inFill(Point())
