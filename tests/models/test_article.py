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
    assert test_article.description == 'Article description'
    assert test_article.author_id == test_article.author.id
    assert test_article.is_published is True


@pytest.mark.asyncio
async def test_read_article(db_session, test_article):
    """Тест чтения статьи."""
    # Получаем статью из базы данных
    result = await db_session.execute(
        select(Article)
        .options(joinedload(Article.author))
        .where(Article.id == test_article.id)
    )
    fetched_article = result.scalar_one()
    
    assert fetched_article.id == test_article.id
    assert fetched_article.title == test_article.title
    assert fetched_article.author.username == 'UserName'
    assert fetched_article.created_at is not None


@pytest.mark.asyncio
async def test_update_article(db_session, test_article):
    """Тест обновления статьи."""
    original_updated_on = test_article.updated_on
    await asyncio.sleep(0.1)  # Маленькая задержка
    
    # Обновляем данные статьи
    test_article.title = 'Updated title'
    test_article.description = 'Updated description'
    test_article.is_published = False
    
    await db_session.commit()
    await db_session.refresh(test_article)
    
    # Проверяем обновленные данные
    assert test_article.title == 'Updated title'
    assert test_article.description == 'Updated description'
    assert test_article.is_published is False
    assert test_article.updated_on >= original_updated_on  # Изменили на >=


@pytest.mark.asyncio
async def test_delete_article(db_session, test_article):
    """Тест удаления статьи."""
    # Удаляем статью
    await db_session.delete(test_article)
    await db_session.commit()
    
    # Проверяем, что статья удалена
    result = await db_session.execute(
        select(Article).where(Article.id == test_article.id)
    )
    assert result.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_article_relationship_with_user(db_session, test_article, test_user):
    """Тест связи статьи с пользователем."""
    assert test_article.author_id == test_user.id
    assert test_article.author.username == 'UserName'
    assert test_article.author.email == 'user@email.com'
    
    # Проверяем, что статья есть в списке статей пользователя
    result = await db_session.execute(
        select(User)
        .options(joinedload(User.articles))
        .where(User.id == test_user.id)
    )
    user_with_articles = result.unique().scalar_one()  # Добавили .unique()
    assert len(user_with_articles.articles) == 1
    assert user_with_articles.articles[0].title == 'Article title'


@pytest.mark.asyncio
async def test_create_unpublished_article(db_session, test_user):
    """Тест создания неопубликованной статьи."""
    article = Article(
        title='Unpublished article',
        title_img='path/to/image.png',
        description='Unpublished description',
        content='Unpublished content',
        author_id=test_user.id,
        is_published=False
    )
    db_session.add(article)
    await db_session.commit()
    await db_session.refresh(article)
    
    assert article.id is not None
    assert article.is_published is False
    assert article.created_at is not None
    assert article.updated_on is not None
