"""Create Item model, used for HTTP Post"""
from pydantic import BaseModel, Field


class CreateItem(BaseModel):
    """CreateItem Model"""
    name: str
    description: str | None
    price: int = Field(ge=0, le=10)
    tax: float | None = None
