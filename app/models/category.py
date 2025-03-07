from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    cover_img = Column(String, nullable=False)
    description = Column(String, index=False)

    articles_category = relationship('Article', back_populates = 'categories')
