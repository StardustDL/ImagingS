from ImagingS.core import RectArea
from abc import ABC, abstractmethod
from ImagingS.core.serialization import PropertySerializable
from typing import List
from ImagingS.core import IdObject
from ImagingS.core.geometry import Geometry
from . import DrawingContext, BoundingAreaMeasurer


class Drawing(PropertySerializable, IdObject, ABC):
    def __init__(self) -> None:
        super().__init__()

    @property
    def clip(self) -> Geometry:
        return self._clip

    @clip.setter
    def clip(self, value: Geometry) -> None:
        self._clip = value

    @abstractmethod
    def render(self, context: DrawingContext) -> None:
        pass

    @property
    def boundingArea(self) -> RectArea:
        if not hasattr(self, "_boundingArea"):
            self._boundingArea = None
            measurer = BoundingAreaMeasurer()
            self.render(measurer)
            self._boundingArea = measurer.end_measure()
        elif self._boundingArea is None:  # boundingArea is calculating
            return RectArea()
        return self._boundingArea

    def refresh_boundingArea(self) -> None:
        if hasattr(self, "_boundingArea"):
            del self._boundingArea


class DrawingGroup(Drawing):
    def __init__(self):
        super().__init__()
        self.children = []

    @property
    def children(self) -> List[Drawing]:
        return self._children

    @children.setter
    def children(self, value: List[Drawing]) -> None:
        self._children = value

    def render(self, context: DrawingContext) -> None:
        for item in self.children:
            item.render(context)
