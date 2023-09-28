from typing import Any
from pydantic import  GetJsonSchemaHandler, GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema, CoreSchema
from bson.objectid import ObjectId


class PyObjectId(ObjectId):
    def __str__(self):
        return self.__class__.__name__

    def __repl__(self):
        return self.__class__.__name__
    @classmethod
    def __get_pydantic_core_schema__(
        _,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> CoreSchema:

        def validate(value: str) -> ObjectId:
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId")
            return ObjectId(value)

        return core_schema.no_info_plain_validator_function(
            function=validate,
            serialization=core_schema.to_string_ser_schema(),
        )


@classmethod
def __get_pydantic_json_schema__(
    cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
) -> JsonSchemaValue:
    return handler(core_schema.str_schema())
