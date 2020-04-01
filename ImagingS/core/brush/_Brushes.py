from ImagingS.core import Colors
from . import SolidBrush, Brush


class Brushes:
    @staticmethod
    def Black() -> Brush:
        result = SolidBrush()
        result.color = Colors.Black()
        return result

    @staticmethod
    def White() -> Brush:
        result = SolidBrush()
        result.color = Colors.White()
        return result

    @staticmethod
    def Red() -> Brush:
        result = SolidBrush()
        result.color = Colors.Red()
        return result

    @staticmethod
    def Blue() -> Brush:
        result = SolidBrush()
        result.color = Colors.Blue()
        return result

    @staticmethod
    def Green() -> Brush:
        result = SolidBrush()
        result.color = Colors.Green()
        return result
