from typing import Generic, Optional, TypeVar

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QGraphicsItem

from ImagingS import Size
from ImagingS.drawing import GeometryDrawing
from ImagingS.geometry import Geometry
from ImagingS.Gui import converters
from ImagingS.Gui.graphic import DrawingItem

from .. import Interactivity

_T = TypeVar("_T")


class GeometryInteractivity(Interactivity, Generic[_T]):
    def __init__(self, target: GeometryDrawing, geometry: _T, size: Size) -> None:
        super().__init__()
        assert isinstance(geometry, Geometry)
        self._target = target
        self._viewItem = DrawingItem(self._target, converters.qsize(size))
        self._geometry = geometry

    @property
    def viewItem(self) -> Optional[QGraphicsItem]:
        return self._viewItem

    @property
    def target(self) -> GeometryDrawing:
        return self._target

    @property
    def geometry(self) -> _T:
        return self._geometry

    def start(self) -> None:
        self.target.geometry = self.geometry
        super().start()

    def end(self, success: bool) -> None:
        if not success:
            self.target.geometry = None
        super().end(success)

    def update(self) -> None:
        self.geometry.refreshBounds()
        super().update()

    def onKeyPress(self, key: QKeyEvent) -> None:
        if key.key() == Qt.Key_Escape:
            self.end(False)
        super().onKeyPress(key)
