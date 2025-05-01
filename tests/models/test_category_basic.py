import pytest

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from datetime import datetime

from app.models.article import Article
from app.models.category import Category


@pytest.mark.asyncio
async def test_category_creation(test_category):
    """Тест создания категории."""
    assert test_category.id is not None
    assert test_category.title == 'Category title'
    assert test_category.is_published is True


@pytest.mark.asyncio
async def test_category_content_field(test_category):
    """Тест полей содержания."""
    assert test_category.description == 'Category description'


@pytest.mark.asyncio
async def test_category_media_field(test_category):
    """Тест медиа-полей."""
    assert test_category.title_img == 'path/media/articles/images/title_img.png'


@pytest.mark.asyncio
async def test_category_date_creation(test_category):
    """Тест даты создания."""
    assert isinstance(test_category.created_at, datetime)
    assert test_category.created_at <= datetime.utcnow()


@pytest.mark.asyncio
async def test_category_retrieval(db_session, test_category):
    """Тест получения категории из БД."""
    result = await db_session.execute(
        select(Category).where(Category.id == test_category.id)
    )
    category = result.scalar_one()
    assert category.title == 'Category title'


@pytest.mark.asyncio
async def test_category_one_article_relationship(db_session, test_category, test_article):
    """Тест связи категории с одной статьей."""
    result = await db_session.execute(
        select(Category).options(joinedload(Category.articles))
        .where(Category.id == test_category.id)
    )
    category = result.unique().scalar_one()
    
    assert len(category.articles) == 1
    assert category.articles[0].id == test_article.id


@pytest.mark.asyncio
async def test_category_articles_relationship(db_session, test_category, test_user):
    """Тест связи категории с несколькими статьями."""
    article_1 = Article(
        title="Article 1",
        description="Description 1",
        content="Content 1",
        title_img="/img1.jpg",
        category_id=test_category.id,
        is_published=True,
        author_id=test_user.id
    )
    article_2 = Article(
        title="Article 2",
        description="Description 2",
        content="Content 2",
        title_img="/img2.jpg",
        category_id=test_category.id,
        is_published=True,
        author_id=test_user.id
    )
    
    db_session.add_all([article_1, article_2])
    await db_session.commit()
    
    result = await db_session.execute(
        select(Category).options(joinedload(Category.articles))
        .where(Category.id == test_category.id)
    )
    category = result.unique().scalar_one()
    
    assert len(category.articles) == 2
    assert {a.title for a in category.articles} == {"Article 1", "Article 2"}


@pytest.mark.asyncio
async def test_category_publishing(db_session, test_category):
    """Тест публикации статьи."""
    test_category.is_published = False

    await db_session.commit()
    await db_session.refresh(test_category)

    assert test_category.is_published is False


@pytest.mark.asyncio
async def test_category_updating(db_session, test_category):
    """Тест обновления категории."""
    test_category.title = 'New category title'

    await db_session.commit()
    await db_session.refresh(test_category)

    assert test_category.title == 'New category title'


@pytest.mark.asyncio
async def test_category_deletion(db_session, test_category):
    """Тест удаления категории."""
    category_id = test_category.id

    await db_session.delete(test_category)
    await db_session.commit()

    deleted = await db_session.get(Category, category_id)
    assert deleted is None


@pytest.mark.asyncio
async def test_category_full_model(db_session, test_category, test_article):
    """."""
    ...
