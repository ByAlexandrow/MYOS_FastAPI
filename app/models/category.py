from datetime import datetime

from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment='ID категории')
    title: Mapped[str] = mapped_column(String(25), unique=True, index=True, comment='Название категории')
    title_img: Mapped[str] = mapped_column(String(255), comment='Титульная картинка')
    description: Mapped[str] = mapped_column(String(50), nullable=False, comment='Краткое описание категории')
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment='Дата создания статьи')
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, comment='Опубликовать категорию')

    articles = relationship('Article', back_populates='category')

    def __repr__(self) -> str:
        return f'{self.title}'


from app.models.article import Article
