from __future__ import annotations
from ImagingS.core.serialization import PropertySerializable
from typing import Dict, Generic, Iterator, Optional, Tuple, TypeVar, List
from math import fabs
import numpy as np

T = TypeVar("T")


class IdObject:
    def __init__(self) -> None:
        super().__init__()
        self.id = ""

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value


class IdObjectList(PropertySerializable, Generic[T]):
    def __init__(self) -> None:
        super().__init__()
        self.items = []

    @property
    def items(self) -> List[T]:
        return self._items

    @items.setter
    def items(self, value: List[T]) -> None:
        if hasattr(self, "_items") and self._items is value:
            return
        self._items: List[T] = []
        self._ids: Dict[str, T] = {}
        for item in value:
            self.append(item)

    def contains(self, key: str) -> bool:
        return key in self._ids

    def append(self, item: T) -> None:
        if self.contains(item.id):
            raise Exception(f"The id '{item.id}' has been added.")
        self._items.append(item)
        self._ids[item.id] = item

    def at(self, index: int) -> T:
        return self._items[index]

    def clear(self) -> None:
        self.items = []

    def __delitem__(self, key: str) -> None:
        if not self.contains(key):
            raise KeyError(key)
        self._items.remove(self._ids[key])
        del self._ids[key]

    def __getitem__(self, key: str) -> T:
        return self._ids[key]

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)


class Point(PropertySerializable):
    def __init__(self) -> None:
        super().__init__()
        self.x = 0
        self.y = 0

    @staticmethod
    def create(x: float, y: float) -> Point:
        result = Point()
        result.x = x
        result.y = y
        return result

    def __eq__(self, other: Point) -> bool:
        return fabs(self.x - other.x) < 1e-8 and fabs(self.y - other.y) < 1e-8

    def __add__(self, other: Point) -> Point:
        return Point.create(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point.create(self.x - other.x, self.y - other.y)

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = value

    def to_array(self) -> np.ndarray:
        return np.array([[self.x], [self.y]])

    def as_tuple(self) -> Tuple[float, float]:
        return self.x, self.y

    @staticmethod
    def from_array(arr: np.ndarray) -> Point:
        assert len(arr) == 2 and len(arr[0]) == 1 and len(arr[1]) == 1
        return Point.create(float(arr[0][0]), float(arr[1][0]))


def _hex_nopre(i: int) -> str:
    return format(i, 'X')


class Color(PropertySerializable):
    def __init__(self) -> None:
        super().__init__()
        self.r = 0
        self.g = 0
        self.b = 0

    @staticmethod
    def create(r: int, g: int, b: int) -> Color:
        result = Color()
        result.r = r
        result.g = g
        result.b = b
        return result

    def __eq__(self, obj) -> bool:
        if isinstance(obj, Color):
            return self.r == obj.r and self.g == obj.g and self.b == obj.b
        return False

    def __repr__(self) -> str:
        return f"Color({self.r}, {self.g}, {self.b})"

    def to_hex(self) -> str:
        return f"#{_hex_nopre(self.r).zfill(2)}{_hex_nopre(self.g).zfill(2)}{_hex_nopre(self.b).zfill(2)}"

    @property
    def r(self) -> int:
        return self._r

    @r.setter
    def r(self, value: int) -> None:
        self._r = value

    @property
    def g(self) -> int:
        return self._g

    @g.setter
    def g(self, value: int) -> None:
        self._g = value

    @property
    def b(self) -> int:
        return self._b

    @b.setter
    def b(self, value: int) -> None:
        self._b = value


class Colors:
    @staticmethod
    def Black() -> Color:
        return Color.create(0, 0, 0)

    @staticmethod
    def White() -> Color:
        return Color.create(255, 255, 255)

    @staticmethod
    def Red() -> Color:
        return Color.create(255, 0, 0)

    @staticmethod
    def Blue() -> Color:
        return Color.create(0, 0, 255)

    @staticmethod
    def Green() -> Color:
        return Color.create(0, 255, 0)


class Size(PropertySerializable):
    def __init__(self) -> None:
        super().__init__()
        self.width = 0
        self.height = 0

    @staticmethod
    def create(width: float, height: float) -> Size:
        result = Size()
        result.width = width
        result.height = height
        return result

    def __eq__(self, obj) -> bool:
        if isinstance(obj, Size):
            return self.width == obj.width and self.height == obj.height
        return False

    def __repr__(self) -> str:
        return f"Size({self.width}, {self.height})"

    def as_tuple(self) -> Tuple[float, float]:
        return self.width, self.height

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        self._width = value

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        self._height = value


class Rect(PropertySerializable):
    __infinite: Optional[Rect] = None

    def __init__(self) -> None:
        super().__init__()
        self.origin = Point()
        self.size = Size()

    @staticmethod
    def create(origin: Point, size: Size) -> Rect:
        result = Rect()
        result.origin = origin
        result.size = size
        return result

    @classmethod
    def infinite(cls) -> Rect:
        if cls.__infinite is None:
            cls.__infinite = Rect.from_points(Point.create(
                float("-inf"), float("-inf")), Point.create(float("inf"), float("inf")))
        return cls.__infinite

    @staticmethod
    def from_points(p1: Point, p2: Point) -> Rect:
        x1, y1 = p1.as_tuple()
        x2, y2 = p2.as_tuple()
        xmin, xmax = min(x1, x2), max(x1, x2)
        ymin, ymax = min(y1, y2), max(y1, y2)
        return Rect.create(Point.create(xmin, ymin), Size.create(xmax - xmin, ymax - ymin))

    def __eq__(self, obj) -> bool:
        if isinstance(obj, Rect):
            return self.origin == obj.origin and self.size == obj.size
        return False

    def __repr__(self) -> str:
        return f"Rect({self.origin}, {self.size})"

    def __contains__(self, point: Point) -> bool:
        delta = point - self.origin
        return 0 <= delta.x <= self.size.width and 0 <= delta.y <= self.size.height

    @property
    def origin(self) -> Point:
        return self._origin

    @origin.setter
    def origin(self, value: Point) -> None:
        self._origin = value

    @property
    def size(self) -> Size:
        return self._size

    @size.setter
    def size(self, value: Size) -> None:
        self._size = value
