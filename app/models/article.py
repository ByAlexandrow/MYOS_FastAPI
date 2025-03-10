from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Carousel(Base):
    __tablename__ = 'carousels'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    article_id = Column(Integer, ForeignKey('articles.id'))

    article = relationship('Article', back_populates='carousel')


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    cover_img = Column(String, nullable=False)
    description = Column(String, nullable=False)
    content = Column(Text, index=True)
    category_id = Column(Integer, ForeignKey('categories.id'))

    categories = relationship('Category', back_populates='articles_category')
    carousel = relationship('Carousel', back_populates='article', uselist=False)
