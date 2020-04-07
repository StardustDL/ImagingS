from enum import Enum
import importlib
import json
from typing import Any, Dict

from . import Serializable


class Encoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Enum):
            return {"__class__": obj.__class__.__name__,
                    "__module__": obj.__module__,
                    "__enumname__": obj.name}
        elif isinstance(obj, Serializable):
            return {"__class__": obj.__class__.__name__,
                    "__module__": obj.__module__,
                    "__data__": obj.serialize()}
        else:
            return super().default(obj)


class Decoder(json.JSONDecoder):
    def __init__(self) -> None:
        json.JSONDecoder.__init__(self, object_hook=Decoder._dict2object)

    @staticmethod
    def _dict2object(dic: Dict) -> Any:
        inst = None
        if "__class__" in dic:
            class_name = dic.pop("__class__")
            module_name = dic.pop("__module__")
            module = importlib.import_module(module_name)
            class_ = getattr(module, class_name)
            if issubclass(class_, Enum):
                name = dic.pop("__enumname__")
                inst = getattr(class_, name)
            elif issubclass(class_, Serializable):
                obj = class_.__call__()
                data = dic.pop("__data__")
                obj.deserialize(data)
                inst = obj
            else:
                raise Exception(
                    f"Type '{module_name}.{class_name}' is not serializable.")
        else:
            inst = dic
        return inst
