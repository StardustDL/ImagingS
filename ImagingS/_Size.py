from __future__ import annotations

from typing import Tuple

from ImagingS.serialization import PropertySerializable


class Size(PropertySerializable):
    def __init__(self, width: float = 0.0, height: float = 0.0) -> None:
        super().__init__()
        self.width = width
        self.height = height

    def __eq__(self, obj: Size) -> bool:
        return self.width == obj.width and self.height == obj.height

    def __repr__(self) -> str:
        return f"Size({self.width}, {self.height})"

    def asTuple(self) -> Tuple[float, float]:
        return self.width, self.height

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        self._width = float(value)

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        self._height = float(value)
