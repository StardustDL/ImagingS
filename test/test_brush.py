from ImagingS import Colors, Point, Rect
from ImagingS.brush import SolidBrush


def test_solid_brush() -> None:
    c = SolidBrush(Colors.Black)
    assert c.colorAt(Point(), Rect()) == Colors.Black
    assert str(c).startswith("SolidBrush")
