
from ImagingS.core import Point
from . import Transform


class Rotate(Transform):
    def __init__(self, center: Point, angle: float) -> None:
        super().__init__()
        self.center = center
        self.angle = angle
