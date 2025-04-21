import pytest

from sqlalchemy import select

from app.models.user import User


@pytest.mark.asyncio
async def test_create_user(test_user):
    """Test async function of creating user model."""
    assert test_user.id is not None
    assert test_user.username == 'UserName'
    assert test_user.email == 'user@email.com'
    assert test_user.hashed_password == 'user_hashed_password'
    assert test_user.bio == 'User bio field'
    assert test_user.is_admin is False


@pytest.mark.asyncio
async def test_read_user(db_session, test_user):
    """Test async function of reading user model."""
    result = await db_session.execute(select(User).filter_by(username=test_user.username))
    user = result.scalar_one_or_none()
    
    assert user is not None
    assert user.username == test_user.username


@pytest.mark.asyncio
async def test_update_user(db_session, test_user):
    """Test async function of updating user model."""
    test_user.bio = 'New user bio'
    
    await db_session.commit()
    await db_session.refresh(test_user)

    assert test_user.bio == 'New user bio'


@pytest.mark.asyncio
async def test_delete_user(db_session, test_user):
    """Test async function of deleting user model."""
    await db_session.delete(test_user)
    await db_session.commit()

    result = await db_session.execute(select(User).filter_by(username=test_user.username))
    user = result.scalar_one_or_none()

    assert user is None
