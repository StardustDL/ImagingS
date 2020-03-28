from abc import ABC
from ImagingS.core import Point, RectArea


class Transform(ABC):
    pass


class Rotate(Transform):
    def __init__(self, center: Point, angle: float) -> None:
        super().__init__()
        self.center = center
        self.angle = angle


class Translate(Transform):
    def __init__(self, delta: Point) -> None:
        super().__init__()
        self.delta = delta


class Scale(Transform):
    def __init__(self, center: Point, factor: float) -> None:
        super().__init__()
        self.center = center
        self.factor = factor


class Skew(Transform):
    def __init__(self) -> None:
        super().__init__()


class Matrix(Transform):
    def __init__(self) -> None:
        super().__init__()


class Clip(Transform):
    def __init__(self, area: RectArea) -> None:
        super().__init__()
        self.area = area
