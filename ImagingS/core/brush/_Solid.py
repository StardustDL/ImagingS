from . import Brush
from ImagingS.core import Color


class Solid(Brush):
    def __init__(self, color: Color) -> None:
        super().__init__()
        self._color = color

    @property
    def color(self) -> Color:
        return self._color
