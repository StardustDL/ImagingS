class Point(object):
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class Size(object):
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height


class RectArea(object):
    def __init__(self, origin: Point, size: Size) -> None:
        self.origin = origin
        self.size = size
