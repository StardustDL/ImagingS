from __future__ import annotations

import uuid
from typing import Collection, Dict, Iterator, List, Optional, TypeVar, Union

from ImagingS.serialization import PropertySerializable


class IdObject:
    def __init__(self, id: str = "") -> None:
        super().__init__()
        self.id = id if id else str(uuid.uuid1())

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = str(value)

    def parent(self) -> Optional[IdObjectList]:
        if hasattr(self, "_parent"):
            return self._parent
        return None

    def setParent(self, value: Optional[IdObjectList]) -> None:
        if value is None:
            if hasattr(self, "_parent"):
                del self._parent
        else:
            self._parent = value


_T = TypeVar("_T", bound=IdObject)


class IdObjectList(PropertySerializable, Collection[_T]):
    def __init__(self) -> None:
        super().__init__()
        self.items = []

    @property
    def items(self) -> List[_T]:
        return self._items

    @items.setter
    def items(self, value: List[_T]) -> None:
        if hasattr(self, "_items") and self._items is value:
            return
        self._items: List[_T] = []
        self._ids: Dict[str, _T] = {}
        for item in value:
            self.append(item)

    def append(self, item: _T) -> None:
        if item.id in self:
            raise Exception(f"The id '{item.id}' has been added.")
        item.setParent(self)
        self._items.append(item)
        self._ids[item.id] = item

    def clear(self) -> None:
        self.items = []

    def setItemId(self, oldId, newId) -> None:
        if oldId not in self._ids:
            return
        if newId in self._ids:
            raise Exception(f"The id '{newId}' has been added.")
        item = self._ids[oldId]
        del self._ids[oldId]
        item.id = newId
        self._ids[item.id] = item

    def __contains__(self, item: Union[str, IdObject]) -> bool:
        if isinstance(item, str):
            return item in self._ids
        else:
            return item.id in self._ids

    def __delitem__(self, key: Union[str, int, IdObject]) -> None:
        if isinstance(key, IdObject):
            key = key.id
        elif isinstance(key, int):
            key = self._items[key].id
        if key not in self:
            return
        item = self._ids[key]
        item.setParent(None)
        self._items.remove(item)
        del self._ids[key]

    def __getitem__(self, key: Union[str, int]) -> _T:
        if isinstance(key, int):
            key = self._items[key].id
        return self._ids[key]

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self) -> Iterator[_T]:
        return iter(self._items)
