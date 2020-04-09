import importlib
import json
from enum import Enum
from typing import Any, Dict, Tuple

from . import Serializable


def _getTypeName(obj: Any) -> str:
    return f"{obj.__module__}::{obj.__class__.__name__}"


def _splitTypeName(s: str) -> Tuple[str, str]:
    ll = list(s.split("::"))
    return ll[0], ll[1]


class Encoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Enum):
            return {"__type__": _getTypeName(obj),
                    "__enum__": obj.name}
        elif isinstance(obj, Serializable):
            result = obj.serialize()
            result["__type__"] = _getTypeName(obj)
            return result
        else:
            return super().default(obj)


class Decoder(json.JSONDecoder):
    def __init__(self) -> None:
        json.JSONDecoder.__init__(self, object_hook=Decoder._dict2object)

    @staticmethod
    def _dict2object(dic: Dict) -> Any:
        inst = None
        if "__type__" in dic:
            moduleName, className = _splitTypeName(dic.pop("__type__"))
            module = importlib.import_module(moduleName)
            class_ = getattr(module, className)
            if issubclass(class_, Enum):
                name = dic.pop("__enum__")
                inst = getattr(class_, name)
            elif issubclass(class_, Serializable):
                obj = class_.__call__()
                obj.deserialize(dic)
                inst = obj
            else:
                raise Exception(
                    f"Type '{moduleName}.{className}' is not serializable.")
        else:
            inst = dic
        return inst
