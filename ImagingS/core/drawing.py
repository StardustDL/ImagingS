from abc import ABC
from ImagingS.core.transform import Transform
from typing import Optional


class Drawing(ABC):
    def __init__(self) -> None:
        self.transform: Optional[Transform] = None
