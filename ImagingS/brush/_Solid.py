from __future__ import annotations

from typing import Optional

from ImagingS import Color, Colors, Point, Rect

from . import Brush


class SolidBrush(Brush):
    def __init__(self, color: Optional[Color] = None) -> None:
        super().__init__()
        self.color = color if color else Colors.Black

    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, value: Color) -> None:
        self._color = value

    def colorAt(self, position: Point, rect: Rect) -> Color:
        return self.color

    def __repr__(self) -> str:
        return f"SolidBrush({self.color})"
