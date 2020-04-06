from ImagingS.core.brush import Brush, Brushes
from ImagingS.core.serialization import PropertySerializable


class Pen(PropertySerializable):
    def __init__(self):
        super().__init__()
        self.thickness = 1
        self.brush = Brushes.Black()

    @property
    def thickness(self) -> float:
        return self._thickness

    @thickness.setter
    def thickness(self, value: float) -> None:
        self._thickness = value

    @property
    def brush(self) -> Brush:
        return self._brush

    @brush.setter
    def brush(self, value: Brush) -> None:
        self._brush = value
