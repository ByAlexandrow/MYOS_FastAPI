from datetime import date

from sqlalchemy import Integer, String, Boolean, Date, event
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment='ID категории')
    title: Mapped[str] = mapped_column(String(25), unique=True, index=True, comment='Название категории')
    title_img: Mapped[str] = mapped_column(String(255), comment='Титульная картинка')
    description: Mapped[str] = mapped_column(String(50), nullable=False, comment='Краткое описание категории')
    created_at: Mapped[date] = mapped_column(Date, server_default=func.current_date(), default=date.today(), comment='Дата создания статьи')
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, comment='Опубликовать категорию')

    articles = relationship('Article', back_populates='category')

    def __repr__(self) -> str:
        return f'{self.title}'


@event.listens_for(Category, 'before_update')
def before_user_update(mapper, connection, target):
    current_created_at = connection.execute(
        Category.__table__.select().with_only_columns(Category.created_at).where(Category.id == target.id)
    ).scalar_one_or_none()

    if target.created_at and current_created_at != target.created_at:
        target.created_at = current_created_at


from app.models.article import Article
