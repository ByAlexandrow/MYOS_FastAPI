from pydantic import BaseModel

from typing import Optional


class CarouselBase(BaseModel):
    title: str
    url: str


class CarouselCreate(CarouselBase):
    article_id: int


class Carousel(CarouselBase):
    id: int
    article_id: int

    class Config:
        orm_mode = True


class ArticleBase(BaseModel):
    title: str
    cover_img: str
    description: str
    content: str
    category_id: int


class ArticleCreate(ArticleBase):
    pass


class Article(ArticleBase):
    id: int
    carousel: Optional[Carousel] = None

    class Config:
        orm_mode = True
