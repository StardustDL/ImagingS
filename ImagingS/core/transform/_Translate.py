from ImagingS.core import Point
from . import Transform


class Translate(Transform):
    def __init__(self, delta: Point) -> None:
        super().__init__()
        self.delta = delta
