from typing import Any, Iterator


class Property:
    def __init__(self, name: str, onwer, prop: property):
        self._name = name
        self._onwer = onwer
        self._get = prop.fget
        self._set = prop.fset
        self._del = prop.fdel
        # self._dataType = prop.fget.__annotations__["return"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def canGet(self) -> bool:
        return self._get is not None

    @property
    def canSet(self) -> bool:
        return self._set is not None

    @property
    def canDel(self) -> bool:
        return self._del is not None

    def get(self) -> Any:
        return self._get.__call__(self._onwer)

    def set(self, val) -> None:
        return self._set.__call__(self._onwer, val)

    def delete(self) -> None:
        return self._del.__call__(self._onwer)


def getProperties(obj: Any) -> Iterator[Property]:
    cls = obj.__class__
    for name in dir(cls):
        item = getattr(cls, name)
        if isinstance(item, property):
            yield Property(name, obj, item)
