import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, joinedload

from app.models.user import User
from app.models.article import Article
from app.models.category import Category
from app.database import Base

TEST_DATABASE_URL = 'sqlite+aiosqlite:///:memory:'

test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture(scope='function')
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='function')
async def db_session(setup_db):
    async with TestSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest.fixture(scope='function')
async def test_user(db_session):
    user = User(
        username='UserName',
        avatar='path/media/user/images/user_avatar.png',
        email='user@email.com',
        hashed_password='user_hashed_password',
        bio='User bio field',
        is_admin=False
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture(scope='function')
async def test_category(db_session):
    category = Category(
        title='Category title',
        title_img='path/media/articles/images/title_img.png',
        description='Category description',
        is_published=True
    )
    db_session.add(category)
    await db_session.commit()
    await db_session.refresh(category)
    return category


@pytest.fixture(scope='function')
async def test_article(db_session, test_user, test_category):
    article = Article(
        title='Article title',
        title_img='path/media/articles/images/title_img.png',
        description='Article description',
        content='Article content',
        audio='path/media/articles/audio/audio.mp3',
        video='path/media/articles/video/video.mp4',
        author_id=test_user.id,
        category_id=test_category.id,
        updated=False,
        is_published=True
    )
    db_session.add(article)
    await db_session.commit()
    await db_session.refresh(article)
    
    result = await db_session.execute(
        select(Article)
        .options(joinedload(Article.author), joinedload(Article.category))
        .filter_by(id=article.id)
    )
    article = result.unique().scalar_one()
    return article
