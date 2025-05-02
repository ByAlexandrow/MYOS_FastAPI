from typing import Optional
from datetime import date

from sqlalchemy import Integer, String, Text, Boolean, Date, event
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    """Модель пользователя."""
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment='ID пользователя')
    username: Mapped[str] = mapped_column(String(30), unique=True, index=True, comment='Имя пользователя')
    avatar: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment='Аватар')
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, comment='Email пользователя')
    hashed_password: Mapped[str] = mapped_column(String(300), comment='Хеш-пароль пользователя')
    bio: Mapped[Optional[str]] = mapped_column(Text(500), nullable=True, comment='О себе')
    created_at: Mapped[date] = mapped_column(Date, server_default=func.current_date(), default=date.today(), nullable=False, comment='Дата регистрации пользователя')
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False, comment='Бан')
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, comment='Администратор')

    articles = relationship('Article', back_populates='author')


    def __repr__(self) -> str:
        return f'{self.username}'


@event.listens_for(User, 'before_update')
def before_user_update(mapper, connection, target):
    current_created_at = connection.execute(
        User.__table__.select().with_only_columns(User.created_at).where(User.id == target.id)
    ).scalar_one_or_none()

    if target.created_at and current_created_at != target.created_at:
        target.created_at = current_created_at


from app.models.article import Article
