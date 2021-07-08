from __future__ import annotations

from typing import Optional

from ImagingS.brush import Brush, Brushes
from ImagingS.serialization import PropertySerializable


class Pen(PropertySerializable):
    def __init__(self, brush: Optional[Brush] = None, thickness: float = 1.0):
        super().__init__()
        self.thickness = 1.0
        self.brush = brush if brush else Brushes.Black

    @property
    def thickness(self) -> float:
        return self._thickness

    @thickness.setter
    def thickness(self, value: float) -> None:
        value = float(value)
        self._thickness = value

    @property
    def brush(self) -> Brush:
        return self._brush

    @brush.setter
    def brush(self, value: Brush) -> None:
        assert isinstance(value, Brush)
        self._brush = value
