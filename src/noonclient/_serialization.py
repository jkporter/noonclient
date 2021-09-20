from json.decoder import WHITESPACE, JSONDecoder
from json.encoder import JSONEncoder
from importlib import import_module
import inspect
from typing import Any, Generic, Type, TypeVar
import dataclasses
import json
import typing
import stringcase

T = TypeVar('T')


def DEFAULT_GET_MODEL(d, model): return model(**d)


_models_module = import_module('noonclient.alaska.model')


def _get_model_fields_types(obj):
    type_hints = typing.get_type_hints(obj)
    return {field.name: type_hints[field.name] for field in dataclasses.fields(obj) if field.name in type_hints}


_models_fields_types = {obj: _get_model_fields_types(obj) for (
    _, obj) in inspect.getmembers(_models_module) if dataclasses.is_dataclass(obj)}


class ModelJSONEncoder(JSONEncoder):
    def default(self, o):
        return {stringcase.spinalcase(k): self.default(v) if isinstance(v, dict) else v for (k, v) in (o if isinstance(o, dict) else dataclasses.asdict(o)).items() if v is not None}


class ModelJSONDecoder(Generic[T], JSONDecoder):

    def __init__(self, get_model=DEFAULT_GET_MODEL, *, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, strict=True, object_pairs_hook=None):
        super(ModelJSONDecoder, self).__init__(object_hook=object_hook, parse_float=parse_float,
                                               parse_int=parse_int, parse_constant=parse_constant, strict=strict, object_pairs_hook=object_pairs_hook)
        self.get_model = get_model

    def decode(self, s, _w=WHITESPACE.match):
        return ModelJSONDecoder.deserialize(JSONDecoder.decode(self, s, _w), typing.get_args(self.__orig_class__)[0], self.get_model)

    @staticmethod
    def deserialize(d: dict, t: Type[T], get_model=DEFAULT_GET_MODEL) -> T:
        def get_value(v, field_type):
            if typing.get_origin(field_type) is list:
                list_model_type = typing.get_args(field_type)[0]
                if list_model_type is not None:
                    return list[list_model_type](ModelJSONDecoder.deserialize(d, list_model_type, get_model) for d in v if isinstance(d, dict))

            if isinstance(v, dict) and field_type in _models_fields_types:
                return ModelJSONDecoder.deserialize(v, field_type, get_model)

            if field_type is Any or isinstance(v, field_type):
                return v

            return None

        def map_to_fields(d):
            for (k, v) in d.items():
                field_name = stringcase.snakecase(k)
                if field_name in _models_fields_types[t]:
                    yield (field_name, get_value(v, _models_fields_types[t][field_name]))

        return get_model(dict(map_to_fields(d)), t)


def _json_seralize(obj):
    return json.dumps(obj, cls=ModelJSONEncoder)


def _get_loads(type: Type, get_model=lambda d, m: m(**d)):
    def loads(s):
        return json.loads(s, cls=ModelJSONDecoder[type], **{'get_model': get_model})
    return loads
