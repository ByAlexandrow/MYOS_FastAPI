import pytest

from app.models.article import Photo


@pytest.mark.asyncio
async def test_create_photo(fixture_create_test_article, fixture_create_test_photo):
    article = fixture_create_test_article
    photo = fixture_create_test_photo

    assert photo.id is not None
    assert photo.url == 'path/to/this/photo.jpg'
    assert photo.article_id == article.id
    assert photo.is_carousel is False 


@pytest.mark.asyncio
async def test_read_photo(db_session, fixture_create_test_article, fixture_create_test_photo):
    article = fixture_create_test_article
    photo = fixture_create_test_photo

    db_photo = await db_session.get(Photo, photo.id)
    assert db_photo is not None
    assert db_photo.url == 'path/to/this/photo.jpg'
    assert db_photo.article_id == article.id
    assert db_photo.is_carousel is False


@pytest.mark.asyncio
async def test_delete_photo(db_session, fixture_create_test_photo):
    photo = fixture_create_test_photo

    await db_session.delete(photo)
    await db_session.commit()

    db_photo = await db_session.get(Photo, photo.id)
    assert db_photo is None