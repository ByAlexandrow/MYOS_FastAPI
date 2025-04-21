import pytest

from sqlalchemy import select

from app.models.article import Article


@pytest.mark.asyncio
async def test_create_article(db_session, test_article, test_user):
    """Test async function of creating article model."""
    assert test_article.id is not None
    assert test_article.title == 'Article title'
    assert test_article.title_img == 'path/to/title_img.jpg'
    assert test_article.description == 'Article description'
    assert test_article.content == 'Article content'
    assert test_article.author_id == test_user.id
    assert test_article.author.username == test_user.username
    assert test_article.is_published is True

    result = await db_session.execute(select(Article).filter_by(id=test_article.id))
    article_from_db = result.scalar_one_or_none()

    assert article_from_db is not None
    assert article_from_db.title == test_article.title


@pytest.mark.asyncio
async def test_read_article(db_session, test_article):
    """Test async function of reading article model."""
    result = await db_session.execute(select(Article).filter_by(title=test_article.title))
    article = result.scalar_one_or_none()

    assert article is not None
    assert article.title == test_article.title


@pytest.mark.asyncio
async def test_update_article(db_session, test_article):
    """Test async function of updating article model."""
    test_article.title = 'New article title'
    test_article.title_img = 'new/path/to/title_img.jpg'
    test_article.description = 'New article description'
    test_article.content = 'New article content'

    await db_session.commit()
    await db_session.refresh(test_article)

    assert test_article.title == 'New article title'
    assert test_article.title_img == 'new/path/to/title_img.jpg'
    assert test_article.description == 'New article description'
    assert test_article.content == 'New article content'


@pytest.mark.asyncio
async def test_delete_article(db_session, test_article):
    """Test async function of deleting article model."""
    await db_session.delete(test_article)
    await db_session.commit()

    result = await db_session.execute(select(Article).filter_by(title=test_article.title))
    article = result.scalar_one_or_none()

    assert article is None
