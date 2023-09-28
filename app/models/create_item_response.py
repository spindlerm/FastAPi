from pydantic import BaseModel,Field,ConfigDict
from .py_objectid import PyObjectId

class CreateItemResponse(BaseModel):
    id: PyObjectId = Field(None,alias='_id')
    name: str
    description: str | None
    price: int = Field(ge=0, le=10)
    tax: float | None = None
    model_config = ConfigDict(arbitrary_types_allowed=True)
