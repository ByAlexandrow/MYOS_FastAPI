import pytest
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.models.user import User


@pytest.mark.asyncio
async def test_create_user(test_user):
    """Тест создания пользователя."""
    assert test_user.id is not None
    assert test_user.username == 'UserName'
    assert test_user.email == 'user@email.com'
    assert test_user.hashed_password == 'user_hashed_password'
    assert test_user.is_admin is False
    assert test_user.created_at is not None


@pytest.mark.asyncio
async def test_read_user(db_session, test_user):
    """Тест чтения пользователя."""
    result = await db_session.execute(
        select(User).where(User.id == test_user.id)
    )
    fetched_user = result.scalar_one()
    
    assert fetched_user.id == test_user.id
    assert fetched_user.username == test_user.username
    assert fetched_user.created_at == test_user.created_at


@pytest.mark.asyncio
async def test_update_user(db_session, test_user):
    """Тест обновления пользователя."""
    # Обновляем данные пользователя
    test_user.username = 'UpdatedName'
    test_user.email = 'updated@email.com'
    test_user.is_admin = True
    
    await db_session.commit()
    await db_session.refresh(test_user)
    
    # Проверяем обновленные данные
    assert test_user.username == 'UpdatedName'
    assert test_user.email == 'updated@email.com'
    assert test_user.is_admin is True


@pytest.mark.asyncio
async def test_delete_user(db_session, test_user):
    """Тест удаления пользователя."""
    # Удаляем пользователя
    await db_session.delete(test_user)
    await db_session.commit()
    
    # Проверяем, что пользователь удален
    result = await db_session.execute(
        select(User).where(User.id == test_user.id)
    )
    assert result.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_user_relationship_with_articles(db_session, test_article, test_user):
    """Тест связи пользователя со статьями."""
    # Проверяем, что статья принадлежит пользователю
    assert test_article.author_id == test_user.id
    
    # Получаем пользователя со статьями
    result = await db_session.execute(
        select(User)
        .options(joinedload(User.articles))
        .where(User.id == test_user.id)
    )
    user_with_articles = result.unique().scalar_one()
    
    assert len(user_with_articles.articles) == 1
    assert user_with_articles.articles[0].title == 'Article title'
    assert user_with_articles.articles[0].id == test_article.id


@pytest.mark.asyncio
async def test_create_user_without_optional_fields(db_session):
    """Тест создания пользователя без необязательных полей."""
    user = User(
        username='MinimalUser',
        email='minimal@email.com',
        hashed_password='minimal_hashed_password'
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    assert user.id is not None
    assert user.avatar is None
    assert user.bio is None
    assert user.is_admin is False


@pytest.mark.asyncio
async def test_unique_constraints(db_session, test_user):
    """Тест уникальных ограничений (username и email)."""
    # Создаем новую сессию для каждого теста уникальности
    async with db_session.begin_nested():
        # Пытаемся создать пользователя с тем же username
        with pytest.raises(Exception):
            user = User(
                username='UserName',  # Дубликат
                email='new@email.com',
                hashed_password='password'
            )
            db_session.add(user)
            await db_session.flush()  # Используем flush вместо commit
    
    async with db_session.begin_nested():
        # Пытаемся создать пользователя с тем же email
        with pytest.raises(Exception):
            user = User(
                username='NewUser',
                email='user@email.com',  # Дубликат
                hashed_password='password'
            )
            db_session.add(user)
            await db_session.flush()
    
    # Явный откат не требуется, так как begin_nested автоматически откатывает при исключении
