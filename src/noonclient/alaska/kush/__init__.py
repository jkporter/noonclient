import dataclasses
from typing import Type
import typing
import stringcase


class GraphQLGenerator:

    @staticmethod
    def generate(type: Type):
        def enumerate(type: Type):
            type_hints = typing.get_type_hints(type)
            fields = {field.name: type_hints[field.name] for field in dataclasses.fields(
                type) if field.name in type_hints}
            yield '{'
            for name, type in fields.items():
                yield stringcase.spinalcase(name)
                type = typing.get_args(type)[0] if typing.get_origin(
                    type) is list else type
                if dataclasses.is_dataclass(type):
                    for s in enumerate(type):
                        yield s
            yield '}'
        return ' '.join(enumerate(type))

