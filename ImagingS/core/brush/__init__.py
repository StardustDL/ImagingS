from abc import ABC
from ._Solid import Solid


class Brush(ABC):
    def __init__(self) -> None:
        super().__init__()


__all__ = (
    "Brush",
    "Solid"
)