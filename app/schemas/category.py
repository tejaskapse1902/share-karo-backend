from pydantic import BaseModel
from typing import Literal

class CategoryCreateSchema(BaseModel):
    role: str
    categories: str
    product: str
    popular: Literal["positive", "negative"]
    category_id: str

class CategoryUpdateSchema(BaseModel):
    role: str | None = None
    categories: str | None = None
    product: str | None = None
    popular: Literal["positive", "negative"] | None = None
