from typing import Generic, Optional, TypeVar, Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QKeyEvent, QPen
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPathItem

from ImagingS.drawing import DrawingGroup
from ImagingS.geometry import Geometry
from ImagingS.transform import TransformGroup

from .. import Interactivity

_T = TypeVar("_T")


class TransformInteractivity(Interactivity, Generic[_T]):
    def __init__(self, target: Union[DrawingGroup, Geometry], transform: _T) -> None:
        super().__init__()
        self._target = target
        self._transform = transform

        self._viewItem = QGraphicsPathItem()
        pen = QPen(QColor("purple"))
        pen.setWidth(1)
        pen.setStyle(Qt.DashLine)
        pen.setCapStyle(Qt.RoundCap)
        self._viewItem.setPen(pen)
        self._viewItem.setBrush(QBrush(QColor("magenta")))

    @property
    def viewItem(self) -> Optional[QGraphicsItem]:
        return self._viewItem

    @property
    def target(self) -> Union[DrawingGroup, Geometry]:
        return self._target

    @property
    def transform(self) -> _T:
        return self._transform

    def start(self) -> None:
        self._oldTransform = self.target.transform
        if isinstance(self._oldTransform, TransformGroup):
            self._oldTransform.children.append(self.transform)
        else:
            self.target.transform = self.transform

        super().start()

    def end(self, success: bool) -> None:
        if not success:
            if isinstance(self._oldTransform, TransformGroup):
                del self._oldTransform.children[self.transform]
            self.target.transform = self._oldTransform
        super().end(success)

    def update(self) -> None:
        self.target.refreshBounds()
        super().update()

    def onKeyPress(self, key: QKeyEvent) -> None:
        if key.key() == Qt.Key_Escape:
            self.end(False)
        super().onKeyPress(key)
