
from ImagingS.core import RectArea, Point
from typing import Optional, Dict, Any
from . import Transform


class ClipTransform(Transform):
    def __init__(self, area: RectArea) -> None:
        super().__init__()
        self._area = area
        self.algorithm = "Cohen-Sutherland"

    @property
    def area(self) -> RectArea:
        return self._area

    def transform(self, origin: Point) -> Optional[Point]:
        raise NotImplementedError()

    @staticmethod
    def deserialize(data: Dict) -> Any:
        result = ClipTransform(data["_area"])
        result.algorithm = data["algorithm"]
        return result
