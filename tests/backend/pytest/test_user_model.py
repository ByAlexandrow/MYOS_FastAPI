import pytest

from app.models.user import SuperUser


@pytest.mark.asyncio
async def test_create_admin(fixture_create_test_admin):
    admin = fixture_create_test_admin

    assert admin.id is not None
    assert admin.username == 'Username'
    assert admin.first_name == 'Name'
    assert admin.last_name == 'Surname'
    assert admin.email == 'admin@mail.ru'
    assert admin.password == '123456789'
    assert admin.is_admin is True


@pytest.mark.asyncio
async def test_read_admin(db_session, fixture_create_test_admin):
    admin = fixture_create_test_admin

    db_admin = await db_session.get(SuperUser, admin.id)
    assert db_admin is not None
    assert db_admin.username == 'Username'
    assert db_admin.first_name == 'Name'
    assert db_admin.last_name == 'Surname'
    assert db_admin.email == 'admin@mail.ru'
    assert db_admin.password == '123456789'
    assert db_admin.is_admin is True
