from ImagingS import Color, IdObject, IdObjectList, Point, Rect, Size


def test_color() -> None:
    c = Color.create(0, 0, 0)
    assert c == Color.create(0, 0, 0)
    assert c.toHex() == "#000000"
    assert str(c).startswith("Color")


def test_point() -> None:
    c = Point.create(1, 1)
    assert +c == c.clone()
    assert -c == Point.create(-1, -1)
    assert c + c == 2 * c
    assert c.asTuple() == (1, 1)
    assert str(c).startswith("Point")
    assert c.toHomogeneous().shape == (3, 1)
    assert c.fromHomogeneous(c.toHomogeneous()) == c


def test_size() -> None:
    c = Size.create(1, 1)
    assert c == Size.create(1, 1)
    assert c.asTuple() == (1, 1)
    assert str(c).startswith("Size")


def test_rect() -> None:
    c = Rect.create(Point.create(1, 1), Size.create(1, 1))
    assert c == Rect.create(Point.create(1, 1), Size.create(1, 1))
    assert c == Rect.from_points(Point.create(1, 2), Point.create(2, 1))
    assert str(c).startswith("Rect")


def test_idobjectlist() -> None:
    ol = IdObjectList()
    obj = IdObject()
    obj.id = "a"
    ol.items = []
    ol.items = ol.items
    assert obj not in ol
    ol.append(obj)
    assert obj in ol
    assert obj.id in ol

    assert len(ol) == 1

    assert ol[0] is obj
    assert ol[obj.id] is obj

    del ol[obj]
    ol.append(obj)
    del ol[0]
    ol.append(obj)
    del ol[obj.id]
