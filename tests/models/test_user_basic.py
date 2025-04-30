import pytest

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models.user import User


@pytest.mark.asyncio
async def test_user_creation(test_user):
    """Тест создания пользователя."""
    assert test_user.id is not None
    assert test_user.username == 'UserName'
    assert test_user.is_admin is False


@pytest.mark.asyncio
async def test_user_defualt_fields(test_user):
    """Тест дефолтный полей модели."""
    assert test_user.avatar == 'path/media/user/images/user_avatar.png'
    assert test_user.created_at is not None


@pytest.mark.asyncio
async def test_user_retrieval(db_session, test_user):
    """Получение пользователя из БД."""
    result = await db_session.execute(
        select(User).where(User.id == test_user.id)
    )
    user = result.scalar_one()
    assert user.username == 'UserName'


@pytest.mark.asyncio
async def test_user_relationship(db_session, test_article, test_user):
    """Тест связи пользователя со статьями."""
    result = await db_session.execute(
        select(User).options(joinedload(User.articles))
        .where(User.id == test_user.id)
    )
    user = result.unique().scalar_one()

    assert len(user.articles) == 1
    assert user.articles[0].title == 'Article title'


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
