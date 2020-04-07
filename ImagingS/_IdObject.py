from __future__ import annotations

from typing import Collection, Dict, Iterator, List, TypeVar, Union

from ImagingS.serialization import PropertySerializable


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
        self._items.append(item)
        self._ids[item.id] = item

    def clear(self) -> None:
        self.items = []

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
            raise KeyError(key)
        self._items.remove(self._ids[key])
        del self._ids[key]

    def __getitem__(self, key: Union[str, int]) -> _T:
        if isinstance(key, int):
            key = self._items[key].id
        return self._ids[key]

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self) -> Iterator[_T]:
        return iter(self._items)
