from abc import ABC
from ImagingS.core.drawing import Drawing
from ImagingS.core.brush import Brushes, Brush


class Geometry(Drawing, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.stroke: Brush = Brushes.Black
        self.fill: Brush = Brushes.White
