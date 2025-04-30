from datetime import datetime

from sqlalchemy import Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class Article(Base):
    """Модель статьи."""
    __tablename__ = 'articles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment='ID статьи')
    title: Mapped[str] = mapped_column(String(25), unique=True, index=True, comment='Название статьи')
    title_img: Mapped[str] = mapped_column(String(255), comment='Титульная картинка')
    description: Mapped[str] = mapped_column(String(50), nullable=False, comment='Краткое описание статьи')
    content: Mapped[str] = mapped_column(Text, comment='Содержание статьи')
    audio: Mapped[str] = mapped_column(String(255), nullable=True, comment='Аудио-подкаст')
    video: Mapped[str] = mapped_column(String(255), nullable=True, comment='Видео-подкаст')
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), comment='ID автора')
    author = relationship('User', back_populates='articles')
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'), comment='ID категории')
    category = relationship('Category', back_populates='articles')
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment='Дата создания статьи')
    updated: Mapped[bool] = mapped_column(Boolean, default=False, comment='Обновление статьи')
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, comment='Опубликовать статью')

    def __repr__(self) -> str:
        return f'{self.title}'


from app.models.user import User
from app.models.category import Category
