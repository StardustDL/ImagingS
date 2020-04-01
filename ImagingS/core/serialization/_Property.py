from typing import Iterator


class Property:
    def __init__(self, name: str, onwer, prop: property):
        self._name = name
        self._onwer = onwer
        self._get = prop.fget
        self._set = prop.fset
        self._del = prop.fdel
        self._data_type = prop.fget.__annotations__["return"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def data_type(self) -> type:
        return self._data_type

    @property
    def can_get(self) -> bool:
        return self._get is not None

    @property
    def can_set(self) -> bool:
        return self._set is not None

    @property
    def can_del(self) -> bool:
        return self._del is not None

    def get(self):
        return self._get.__call__(self._onwer)

    def set(self, val):
        return self._set.__call__(self._onwer, val)

    def delete(self):
        return self._del.__call__(self._onwer)


def get_properties(obj) -> Iterator[Property]:
    cls = obj.__class__
    for name in dir(cls):
        item = getattr(cls, name)
        if isinstance(item, property):
            yield Property(name, obj, item)
