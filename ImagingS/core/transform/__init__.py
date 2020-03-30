from abc import ABC
from ._Clip import Clip
from ._Matrix import Matrix
from ._Rotate import Rotate
from ._Scale import Scale
from ._Skew import Skew
from ._Translate import Translate


class Transform(ABC):
    def __init__(self):
        super().__init__()


__all__ = (
    "Transform",
    "Clip",
    "Matrix",
    "Rotate",
    "Scale",
    "Skew",
    "Translate",
)
