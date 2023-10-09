"""Update Item model, used for HTTP Post"""
from typing import Optional
from pydantic import BaseModel, Field


class UpdateItem(BaseModel):
    """UpdateItem Model"""

    name: str | None
    description: Optional[str] = None
    price: int = Field(None, ge=0, le=10)
    tax: float | None = None
