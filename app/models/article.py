from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    cover_img = Column(String, nullable=False)
    description = Column(String, nullable=False)
    content = Column(Text, index=True)
    category_id = Column(Integer, ForeignKey('categories.id'))

    categories = relationship('Category', back_populates = 'articles_category')
