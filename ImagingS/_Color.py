from __future__ import annotations

from ImagingS.serialization import PropertySerializable


def _hexNopre(i: int) -> str:
    return format(i, 'X')


class Color(PropertySerializable):
    def __init__(self, r: int = 0, g: int = 0, b: int = 0) -> None:
        super().__init__()
        self.r = r
        self.g = g
        self.b = b

    def __eq__(self, obj: Color) -> bool:
        return self.r == obj.r and self.g == obj.g and self.b == obj.b

    def __repr__(self) -> str:
        return f"Color({self.r}, {self.g}, {self.b})"

    def toHex(self) -> str:
        return f"#{_hexNopre(self.r).zfill(2)}{_hexNopre(self.g).zfill(2)}{_hexNopre(self.b).zfill(2)}"

    @staticmethod
    def fromHex(h: str) -> Color:
        h = h.lstrip("#").zfill(6)[0:6]
        return Color(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

    @property
    def r(self) -> int:
        return self._r

    @r.setter
    def r(self, value: int) -> None:
        self._r = int(value)

    @property
    def g(self) -> int:
        return self._g

    @g.setter
    def g(self, value: int) -> None:
        self._g = int(value)

    @property
    def b(self) -> int:
        return self._b

    @b.setter
    def b(self, value: int) -> None:
        self._b = int(value)


class Colors:
    Black = Color(0, 0, 0)
    White = Color(255, 255, 255)
    Red = Color(255, 0, 0)
    Blue = Color(0, 0, 255)
    Green = Color(0, 255, 0)
