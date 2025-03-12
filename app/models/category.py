from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    cover_img = Column(String, nullable=False)
    description = Column(String, index=False)
    is_published = Column(Boolean, index=True, default=False)

    article = relationship('Article', back_populates='category')

    def __repr__(self):
        return self.title
