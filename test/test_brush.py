from ImagingS import Colors, Point, Rect
from ImagingS.brush import SolidBrush


def test_solid_brush() -> None:
    c = SolidBrush.create(Colors.Black)
    assert c.color_at(Point(), Rect()) == Colors.Black
    assert str(c).startswith("SolidBrush")