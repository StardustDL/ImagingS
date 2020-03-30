
from ImagingS.core import RectArea
from . import Transform


class Clip(Transform):
    def __init__(self, area: RectArea) -> None:
        super().__init__()
        self.area = area
