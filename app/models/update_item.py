"""Update Item model, used for HTTP Post"""
from typing import Optional
from pydantic import BaseModel, Field


class UpdateItem(BaseModel):
    """UpdateItem Model"""

    # All fields are optional for the update/Put operations

    name: str | None = None
    description: str | None = None
    price: int = Field(None, ge=0, le=10)
    tax: float  = None
