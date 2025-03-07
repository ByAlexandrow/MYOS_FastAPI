import pytest

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.category import Category
from app.models.article import Article, Photo


DATABASE_URL = 'sqlite+aiosqlite:///./test.db'


engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)


@pytest.fixture(scope='function')
async def test_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='function')
async def db_session(test_db):
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture(scope='function')
async def fixture_create_test_category(db_session):
    test_category = Category(
        title='Test Category',
        cover_img='path/to/category_img.jpg',
        description='This is a test category!'
    )
    db_session.add(test_category)
    await db_session.commit()
    await db_session.refresh(test_category)

    return test_category


@pytest.fixture(scope='function')
async def fixture_create_test_article(db_session):
    test_article = Article(
        title='Test Article',
        cover_img='path/to/article_img.jpg',
        description='This is a test article!',
        content='Here will be a content for the article!'
    )
    db_session.add(test_article)
    await db_session.commit()
    await db_session.refresh(test_article)

    return test_article


@pytest.fixture(scope='function')
async def fixture_create_test_photo(db_session, fixture_create_test_article):
    article = fixture_create_test_article

    test_photo = Photo(
        url='path/to/this/photo.jpg',
        article_id=article.id,
        is_carousel=False
    )
    db_session.add(test_photo)
    await db_session.commit()
    await db_session.refresh(test_photo)

    return test_photo