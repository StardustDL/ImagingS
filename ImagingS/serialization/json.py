import importlib
import json
from typing import Any, Dict

from . import Serializable


class Encoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Serializable):
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
        if "__class__" in dic:
            class_name = dic.pop("__class__")
            module_name = dic.pop("__module__")
            module = importlib.import_module(module_name)
            class_ = getattr(module, class_name)
            obj = class_.__call__(class_)
            if isinstance(obj, Serializable):
                data = dic.pop("__data__")
                obj.deserialize(data)
            else:
                raise Exception(
                    f"Type '{module_name}.{class_name}' is not serializable.")
            inst = obj
        else:
            inst = dic
        return inst
