from pydantic import BaseModel, Field


class CreateItem(BaseModel):
    name: str
    description: str | None
    price: int = Field(ge=0, le=10)
    tax: float | None = None
