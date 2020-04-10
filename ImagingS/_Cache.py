from typing import Any


class Cache:
    def __init__(self) -> None:
        super().__init__()
        self._dict = {}

    def update(self, key: Any, value: Any) -> None:
        self._dict[key] = value

    def outdate(self, key: Any = None) -> None:
        if key is None:
            self._dict.clear()
        elif key in self._dict:
            del self._dict[key]

    def __getitem__(self, key: Any) -> Any:
        if key in self._dict:
            return self._dict[key]
        return None

    def __contains__(self, key: Any) -> bool:
        return key in self._dict
