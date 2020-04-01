
from ImagingS.core import RectArea
from . import Transform


class ClipTransform(Transform):
    def __init__(self, area: RectArea) -> None:
        super().__init__()
        self._area = area

    @property
    def area(self) -> RectArea:
        return self._area
