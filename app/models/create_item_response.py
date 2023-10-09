"""Create Item model response object, used for HTTP Post response"""
from pydantic import BaseModel, Field, ConfigDict
from pydantic_mongo import ObjectIdField


class CreateItemResponse(BaseModel):
    """Create Item Response Model object, used for HTTP Post response"""

    id: ObjectIdField = Field(None, alias="_id")
    name: str
    description: str | None
    price: int = Field(ge=0, le=10)
    tax: float | None = None
    model_config = ConfigDict(arbitrary_types_allowed=True)
