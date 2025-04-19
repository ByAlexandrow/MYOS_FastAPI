from typing import Optional, List
from datetime import datetime

from sqlalchemy import Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    """Модель пользователя."""
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment='ID пользователя')
    username: Mapped[str] = mapped_column(String(30), unique=True, index=True, comment='Логин пользователя')
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, comment='Email пользователя')
    hashed_password: Mapped[str] = mapped_column(String(300), comment='Хеш-пароль пользователя')
    bio: Mapped[Optional[str]] = mapped_column(Text(500), nullable=True, comment='О себе')
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, comment='Администратор')
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment='Дата регистрации пользователя')

    articles = relationship('Article', back_populates='author')

    def __repr__(self) -> str:
        return f'{self.username}'
