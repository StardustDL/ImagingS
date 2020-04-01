from typing import Optional, Dict, Any
from ImagingS.core import Point
from . import Transform


class TranslateTransform(Transform):
    def __init__(self, delta: Point) -> None:
        super().__init__()
        self._delta = delta

    @property
    def delta(self) -> Point:
        return self._delta

    def transform(self, origin: Point) -> Optional[Point]:
        return origin + self._delta

    @staticmethod
    def deserialize(data: Dict) -> Any:
        result = TranslateTransform(data["_delta"])
        return result
