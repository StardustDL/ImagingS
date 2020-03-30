from ImagingS.core.brush import Brush, brushes
from ImagingS.core.drawing import Drawing
from ._Line import Line
from ._Ellipse import Ellipse
from ._Curve import Curve
from ._Polygon import Polygon


class Geometry(Drawing):
    def __init__(self) -> None:
        super().__init__()
        self.stroke: Brush = brushes.Black
        self.fill: Brush = brushes.White


__all__ = (
    "Geometry",
    "Line",
    "Ellipse",
    "Curve",
    "Polygon"
)
