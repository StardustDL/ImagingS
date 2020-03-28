from ImagingS.core import RectArea
from . import Geometry


class Ellipse(Geometry):
    def __init__(self, area: RectArea) -> None:
        super().__init__()
        self.area = area
