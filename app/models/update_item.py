"""Update Item model, used for HTTP Post"""
from typing import Optional
from pydantic import BaseModel, Field


class UpdateItem(BaseModel):
    """UpdateItem Model"""

    name: str | None
    description: str | None
    price: int = Field(ge=0, le=10)
    tax: float  
