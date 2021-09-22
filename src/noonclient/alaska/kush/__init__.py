import dataclasses
from typing import Type
import typing


class GraphQLGenerator:

    @staticmethod
    def generate(type: Type):
        def enumerate(type: Type):
            def serializedname(name: str):
                return type._serializednames[name] if name in type._serializednames else name
            transname = serializedname if hasattr(
                type, '_serializednames') else lambda x: x
            type_hints = typing.get_type_hints(type)
            fields = {transname(field.name): type_hints[field.name] for field in dataclasses.fields(
                type) if field.name in type_hints}
            yield '{'
            for name, type in fields.items():
                yield name
                type = typing.get_args(type)[0] if typing.get_origin(
                    type) is list else type
                if dataclasses.is_dataclass(type):
                    for s in enumerate(type):
                        yield s
            yield '}'
        return ' '.join(enumerate(type))
