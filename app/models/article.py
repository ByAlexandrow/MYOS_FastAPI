from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Carousel(Base):
    __tablename__ = 'carousels'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    is_published = Column(Boolean, index=True, default=False)
    article_id = Column(Integer, ForeignKey('articles.id'))

    article = relationship('Article', back_populates='carousel')


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    cover_img = Column(String, nullable=False)
    description = Column(String, nullable=False)
    content = Column(Text, index=True)
    pdf = Column(String, nullable=True)
    is_published = Column(Boolean, index=True, default=False)
    category_id = Column(Integer, ForeignKey('categories.id'))

    categories = relationship('Category', back_populates='articles_category')
    carousel = relationship('Carousel', back_populates='article', uselist=False)
