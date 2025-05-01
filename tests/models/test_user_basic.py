import pytest

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from datetime import datetime

from app.models.user import User
from app.models.article import Article


@pytest.mark.asyncio
async def test_user_creation(test_user):
    """Тест создания пользователя."""
    assert test_user.id is not None
    assert test_user.username == 'UserName'
    assert test_user.is_admin is False


@pytest.mark.asyncio
async def test_user_content_field(test_user):
    """Тест полей содержания."""
    assert test_user.bio == 'User bio field'


@pytest.mark.asyncio
async def test_user_mdeia_fields(test_user):
    """Тест медиа-полей"""
    assert test_user.avatar == 'path/media/user/images/user_avatar.png'


@pytest.mark.asyncio
async def test_user_date_creation(test_user):
    """Тест даты создания."""
    assert isinstance(test_user.created_at, datetime)
    assert test_user.created_at <= datetime.utcnow()


@pytest.mark.asyncio
async def test_user_retrieval(db_session, test_user):
    """Тест получения пользователя из БД."""
    result = await db_session.execute(
        select(User).where(User.id == test_user.id)
    )
    user = result.scalar_one()
    assert user.username == 'UserName'


@pytest.mark.asyncio
async def test_user_one_article_relationship(db_session, test_user, test_article):
    """Тест связи пользователя с одной статьей."""
    result = await db_session.execute(
        select(User).options(joinedload(User.articles))
        .where(User.id == test_user.id)
    )
    user = result.unique().scalar_one()

    assert len(user.articles) == 1
    assert user.articles[0].title == test_article.title


@pytest.mark.asyncio
async def test_user_articles_relationship(db_session, test_user, test_category):
    """Тест связи пользователя с несколькими статьями."""
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
        select(User)
        .options(joinedload(User.articles))
        .where(User.id == test_user.id)
    )
    user = result.unique().scalar_one()

    assert len(user.articles) == 2
    assert {a.title for a in user.articles} == {"Article 1", "Article 2"}


@pytest.mark.asyncio
async def test_user_update(db_session, test_user):
    """Тест обновления пользователя."""
    test_user.username = 'NewUserName'
    
    await db_session.commit()
    await db_session.refresh(test_user)

    updated = await db_session.get(User, test_user.id)
    assert updated.username == 'NewUserName'


@pytest.mark.asyncio
async def test_user_deletion(db_session, test_user):
    """Тест удаления пользователя."""
    user_id = test_user.id

    await db_session.delete(test_user)
    await db_session.commit()

    deleted = await db_session.get(User, user_id)
    assert deleted is None


@pytest.mark.asyncio
async def test_user_password_security(test_user):
    """Тест хэширования пароля."""
    assert test_user.hashed_password != 'simple_password'
    assert len(test_user.hashed_password) > 0
