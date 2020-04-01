from abc import ABC
from ImagingS.core.drawing import Drawing
from ImagingS.core.brush import Brushes, Brush


class Geometry(Drawing, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.stroke = Brushes.Black()
        self.fill = Brushes.White()

    @property
    def stroke(self) -> Brush:
        return self._stroke

    @stroke.setter
    def stroke(self, value: Brush) -> None:
        self._stroke = value

    @property
    def fill(self) -> Brush:
        return self._fill

    @fill.setter
    def fill(self, value: Brush) -> None:
        self._fill = value
