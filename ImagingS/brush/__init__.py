from ._Brush import Brush
from ._Solid import SolidBrush
from ImagingS import Colors

__all__ = (
    "Brush",
    "SolidBrush",
    "Brushes"
)


class Brushes:
    Black = SolidBrush(Colors.Black)
    White = SolidBrush(Colors.White)
    Red = SolidBrush(Colors.Red)
    Blue = SolidBrush(Colors.Blue)
    Green = SolidBrush(Colors.Green)
