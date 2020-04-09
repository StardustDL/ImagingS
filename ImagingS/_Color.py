from __future__ import annotations

from ImagingS.serialization import PropertySerializable


def _hexNopre(i: int) -> str:
    return format(i, 'X')


class Color(PropertySerializable):
    def __init__(self) -> None:
        super().__init__()
        self.r = 0
        self.g = 0
        self.b = 0

    @staticmethod
    def create(r: int, g: int, b: int) -> Color:
        result = Color()
        result.r = r
        result.g = g
        result.b = b
        return result

    def __eq__(self, obj: Color) -> bool:
        return self.r == obj.r and self.g == obj.g and self.b == obj.b

    def __repr__(self) -> str:
        return f"Color({self.r}, {self.g}, {self.b})"

    def toHex(self) -> str:
        return f"#{_hexNopre(self.r).zfill(2)}{_hexNopre(self.g).zfill(2)}{_hexNopre(self.b).zfill(2)}"

    @property
    def r(self) -> int:
        return self._r

    @r.setter
    def r(self, value: int) -> None:
        self._r = value

    @property
    def g(self) -> int:
        return self._g

    @g.setter
    def g(self, value: int) -> None:
        self._g = value

    @property
    def b(self) -> int:
        return self._b

    @b.setter
    def b(self, value: int) -> None:
        self._b = value


class Colors:
    Black = Color.create(0, 0, 0)
    White = Color.create(255, 255, 255)
    Red = Color.create(255, 0, 0)
    Blue = Color.create(0, 0, 255)
    Green = Color.create(0, 255, 0)
