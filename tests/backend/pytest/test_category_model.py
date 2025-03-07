import pytest

from app.models.category import Category


@pytest.mark.asyncio
async def test_create_category(fixture_create_test_category):
    category = fixture_create_test_category

    assert category.id is not None
    assert category.title == 'Test Category'
    assert category.cover_img == 'path/to/category_img.jpg'
    assert category.description == 'This is a test category!'


@pytest.mark.asyncio
async def test_read_category(db_session, fixture_create_test_category):
    category = fixture_create_test_category

    db_category = await db_session.get(Category, category.id)
    assert db_category is not None
    assert db_category.title == 'Test Category'
    assert db_category.cover_img == 'path/to/category_img.jpg'
    assert db_category.description == 'This is a test category!'
