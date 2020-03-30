from ImagingS.core import Point
from . import Transform


class Scale(Transform):
    def __init__(self, center: Point, factor: float) -> None:
        super().__init__()
        self.center = center
        self.factor = factor
