from pydantic import BaseModel

from typing import List, Optional


class CategoryBase(BaseModel):
    title: str
    cover_img: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    id: int
    articles_category: List[int] = []

    class Config:
        orm_mode = True
