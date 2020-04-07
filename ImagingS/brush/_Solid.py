from __future__ import annotations

from ImagingS import Color, Colors, Point, Rect

from . import Brush


class SolidBrush(Brush):
    def __init__(self) -> None:
        super().__init__()
        self.color = Colors.Black

    @staticmethod
    def create(color: Color) -> SolidBrush:
        result = SolidBrush()
        result.color = color
        return result

    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, value: Color) -> None:
        self._color = value

    def color_at(self, position: Point, area: Rect) -> Color:
        return self.color

    def __repr__(self) -> str:
        return f"SolidBrush({self.color})"
