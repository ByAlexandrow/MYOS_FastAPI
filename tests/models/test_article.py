import pytest
import asyncio
from sqlalchemy import select
from app.models.article import Article
from app.models.user import User
from sqlalchemy.orm import joinedload


@pytest.mark.asyncio
async def test_create_article(test_article):
    """Тест создания статьи."""
    assert test_article.id is not None
    assert test_article.title == 'Article title'
    assert test_article.title_img == 'path/media/articles/images/title_img.png'
    assert test_article.description == 'Article description'
    assert test_article.content == 'Article content'
    assert test_article.audio == 'path/media/articles/audio/audio.mp3'
    assert test_article.video == 'path/media/articles/video/video.mp4'
    assert test_article.author_id == test_article.author.id
    assert test_article.created_at is not None
    assert test_article.updated_on is False
    assert test_article.is_published is True


@pytest.mark.asyncio
async def test_read_article(db_session, test_article):
    """Тест чтения статьи."""
    result = await db_session.execute(
        select(Article).options(joinedload(Article.author))
        .where(Article.id == test_article.id)
    )
    fetched_article = result.scalar_one()
    
    assert fetched_article.id == test_article.id
    assert fetched_article.title == test_article.title
    assert fetched_article.title_img == test_article.title_img
    assert fetched_article.description == test_article.description
    assert fetched_article.content == test_article.content
    assert fetched_article.audio == test_article.audio
    assert fetched_article.video == test_article.video
    assert fetched_article.author.username == 'UserName'
    assert fetched_article.created_at is not None
    assert fetched_article.updated_on == test_article.updated_on
    assert fetched_article.is_published == test_article.is_published


@pytest.mark.asyncio
async def test_update_article(db_session, test_article):
    """Тест обновления статьи."""
    original_updated_on = test_article.updated_on
    await asyncio.sleep(0.5)
    
    test_article.title = 'Updated Artcile title'
    test_article.description = 'Updated Article description'
    test_article.content = 'Updated Article content'
    test_article.audio = 'updated_path/media/articles/audio/audio.mp3'
    test_article.video = 'updated_path/media/articles/video/video.mp4'
    test_article.created_at is not None
    test_article.updated_on = True
    test_article.is_published = True
    
    await db_session.commit()
    await db_session.refresh(test_article)
    
    assert test_article.title == 'Updated Artcile title'
    assert test_article.description == 'Updated Article description'
    assert test_article.content == 'Updated Article content'
    assert test_article.audio == 'updated_path/media/articles/audio/audio.mp3'
    assert test_article.video == 'updated_path/media/articles/video/video.mp4'    
    assert test_article.created_at is not None
    assert test_article.updated_on is True
    assert test_article.is_published is True


@pytest.mark.asyncio
async def test_delete_article(db_session, test_article):
    """Тест удаления статьи."""
    await db_session.delete(test_article)
    await db_session.commit()

    result = await db_session.execute(
        select(Article).where(Article.id == test_article.id)
    )
    assert result.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_article_relationship_with_user(db_session, test_article, test_user):
    """Тест связи статьи с пользователем."""
    assert test_article.author_id == test_user.id
    assert test_article.author.username == 'UserName'
    assert test_article.author.avatar == 'path/media/user/images/user_avatar.png'
    assert test_article.author.email == 'user@email.com'

    result = await db_session.execute(
        select(User).options(joinedload(User.articles))
        .where(User.id == test_user.id)
    )
    user_with_articles = result.unique().scalar_one()
    
    assert len(user_with_articles.articles) == 1
    assert user_with_articles.articles[0].id == test_article.id
    assert user_with_articles.articles[0].title == 'Article title'
    assert user_with_articles.articles[0].title_img == 'path/media/articles/images/title_img.png'
    assert user_with_articles.articles[0].description == 'Article description'
    assert user_with_articles.articles[0].content == 'Article content'
    assert user_with_articles.articles[0].audio == 'path/media/articles/audio/audio.mp3'
    assert user_with_articles.articles[0].video == 'path/media/articles/video/video.mp4'
    assert user_with_articles.articles[0].author_id == test_article.author.id
    assert user_with_articles.articles[0].updated_on is False
    assert user_with_articles.articles[0].is_published is True
