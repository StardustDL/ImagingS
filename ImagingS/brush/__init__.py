from ._Brush import Brush
from ._Solid import SolidBrush
from ImagingS import Colors

__all__ = (
    "Brush",
    "SolidBrush",
    "Brushes"
)


class Brushes:
    Black = SolidBrush.create(Colors.Black)
    White = SolidBrush.create(Colors.White)
    Red = SolidBrush.create(Colors.Red)
    Blue = SolidBrush.create(Colors.Blue)
    Green = SolidBrush.create(Colors.Green)
