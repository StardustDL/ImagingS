import importlib
import json

from . import Serializable


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Serializable):
            return {"__class__": obj.__class__.__name__,
                    "__module__": obj.__module__,
                    "__data__": obj.serialize()}
        else:
            return super().default(obj)


class Decoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict2object)

    def dict2object(self, d):
        if "__class__" in d:
            class_name = d.pop("__class__")
            module_name = d.pop("__module__")
            module = importlib.import_module(module_name)
            class_ = getattr(module, class_name)
            obj = class_.__new__(class_)
            class_.__init__(obj)
            if isinstance(obj, Serializable):
                data = d.pop("__data__")
                obj.deserialize(data)
            else:
                raise Exception(
                    f"Type '{module_name}.{class_name}' is not serializable.")
            inst = obj
        else:
            inst = d
        return inst
