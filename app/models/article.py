from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    article_id = Column(Integer, ForeignKey('articles.id', ondelete='CASCADE'))
    is_carousel = Column(Boolean, default=False)

    articles_photos = relationship('Article', back_populates='photos')


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    cover_img = Column(String, nullable=False)
    description = Column(String, nullable=False)
    content = Column(Text, index=True)
    category_id = Column(Integer, ForeignKey('categories.id'))

    categories = relationship('Category', back_populates = 'articles_category')
    photos = relationship('Photo', back_populates='articles_photos', cascade='all, delete-orphan')

    @property
    def carousel_photos(self):
        return [photo for photo in self.photos if photo.is_carousel]
    

    @property
    def one_photo(self):
        return [photo for photo in self.photos if not photo.is_carousel[:5]]
