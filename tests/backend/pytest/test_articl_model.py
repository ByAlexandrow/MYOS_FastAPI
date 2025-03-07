import pytest

from app.models.article import Article


@pytest.mark.asyncio
async def test_create_article(fixture_create_test_article):
    article = fixture_create_test_article

    assert article.id is not None
    assert article.title == 'Test Article'
    assert article.cover_img == 'path/to/article_img.jpg'
    assert article.description == 'This is a test article!'
    assert article.content == 'Here will be a content for the article!'


@pytest.mark.asyncio
async def test_read_article(db_session, fixture_create_test_article):
    article = fixture_create_test_article

    db_article = await db_session.get(Article, article.id)
    assert db_article is not None
    assert db_article.title == 'Test Article'
    assert db_article.cover_img == 'path/to/article_img.jpg'
    assert db_article.description == 'This is a test article!'
    assert db_article.content == 'Here will be a content for the article!'
