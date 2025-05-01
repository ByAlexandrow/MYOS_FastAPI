import pytest

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from datetime import datetime

from app.models.user import User
from app.models.article import Article
from app.models.category import Category


@pytest.mark.asyncio
async def test_article_creation(test_article):
    """Тест базового создания статьи."""
    assert test_article.id is not None
    assert test_article.title == 'Article title'
    assert test_article.is_published is True


@pytest.mark.asyncio
async def test_article_content_fields(test_article):
    """Тест полей содержания."""
    assert test_article.description == 'Article description'
    assert test_article.content == 'Article content'


@pytest.mark.asyncio
async def test_article_media_fields(test_article):
    """Тесты медиа-полей."""
    assert test_article.title_img == 'path/media/articles/images/title_img.png'
    assert test_article.audio == 'path/media/articles/audio/audio.mp3'
    assert test_article.video == 'path/media/articles/video/video.mp4'


@pytest.mark.asyncio
async def test_article_date_creation(test_article):
    """Тест даты создания."""
    assert isinstance(test_article.created_at, datetime)
    assert test_article.created_at <= datetime.utcnow()


@pytest.mark.asyncio
async def test_article_retrieval(db_session, test_article):
    """Тест получения статьи из БД."""
    result = await db_session.execute(
        select(Article).where(Article.id == test_article.id)
    )
    article = result.scalar_one()
    assert article.title == 'Article title'


@pytest.mark.asyncio
async def test_artcile_author_relationship(test_article, test_user):
    """Тест связи статьи с автором."""
    assert test_article.author_id == test_user.id
    assert test_article.author.username == 'UserName'


@pytest.mark.asyncio
async def test_article_category_relationship(test_article, test_category):
    """Тест связи статьи с категорией."""
    assert test_article.category_id == test_category.id
    assert test_article.category.title == 'Category title'


@pytest.mark.asyncio
async def test_article_publishing(db_session, test_article):
    """Тест публикации статьи."""
    test_article.is_published = False
    
    await db_session.commit()
    await db_session.refresh(test_article)
    
    assert test_article.is_published is False


@pytest.mark.asyncio
async def test_article_updating(db_session, test_article):
    """Тест обновления статьи."""
    assert test_article.updated is False

    test_article.title = 'New article title'
    test_article.updated = True

    await db_session.commit()
    await db_session.refresh(test_article)

    assert test_article.title == 'New article title'
    assert test_article.updated is True


@pytest.mark.asyncio
async def test_article_deletion(db_session, test_article):
    """Тест удаления статьи."""
    article_id = test_article.id

    await db_session.delete(test_article)
    await db_session.commit()

    deleted = await db_session.get(Article, article_id)
    assert deleted is None


@pytest.mark.asyncio
async def test_article_full_model(db_session, test_user, test_category):
    """Комплексный тест модели статьей."""
    # Тест создания статьи
    article = Article(
        title='Check full model',
        title_img='path/media/articles/images/title_img.png',
        description='Full model description',
        content='Full model content',
        audio='path/media/articles/audio/audio.mp3',
        video='path/media/articles/video/video.mp4',
        author_id=test_user.id,
        category_id=test_category.id,
        updated=False,
        is_published=False
    )
    db_session.add(article)
    await db_session.commit()
    await db_session.refresh(article)

    # Проверка базовых полей модели
    assert article.id is not None
    assert article.title == 'Check full model'
    assert article.title_img == 'path/media/articles/images/title_img.png'
    assert article.description == 'Full model description'
    assert article.content == 'Full model content'
    assert article.audio == 'path/media/articles/audio/audio.mp3'
    assert article.video == 'path/media/articles/video/video.mp4'
    assert article.created_at is not None
    assert article.updated is False
    assert article.is_published is False

    # Проверка связей модели (ленивая загрузка)
    assert article.author_id == test_user.id
    assert article.category_id == test_category.id

    # Проверка связей модели (joinedload)
    result = await db_session.execute(
        select(Article).options(joinedload(Article.author), joinedload(Article.category))
        .where(Article.id == article.id)
    )
    loaded_article = result.unique().scalar_one()

    assert loaded_article.author.username == test_user.username
    assert loaded_article.category.title == test_category.title

    # Тест обновления статьи
    original_created_at = article.created_at

    article.title = 'Updated article title'
    article.description = 'Updated article description'
    article.updated = True
    article.is_published = True

    await db_session.commit()
    await db_session.refresh(article)

    assert article.title == 'Updated article title'
    assert article.description == 'Updated article description'
    assert article.updated is True
    assert article.is_published is True
    assert article.created_at == original_created_at

    # Тест удаления статьи
    article_id = article.id

    await db_session.delete(article)
    await db_session.commit()

    deleted_article = await db_session.get(Article, article_id)
    assert deleted_article is None

    # Проверка каскадных операций
    assert await db_session.get(User, test_user.id) is not None
    assert await db_session.get(Category, test_category.id) is not None
