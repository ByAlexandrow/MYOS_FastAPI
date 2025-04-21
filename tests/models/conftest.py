import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, joinedload

from app.models.user import User
from app.models.article import Article
# from app.models.category import Category
from app.database import Base

TEST_DATABASE_URL = 'sqlite+aiosqlite:///:memory:'

test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=True
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
        yield session


@pytest.fixture(scope='function')
async def test_user(db_session):
    user = User(
        username='UserName',
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
async def test_article(db_session, test_user):
    article = Article(
        title='Article title',
        title_img='path/to/title_img.jpg',
        description='Article description',
        content='Article content',
        author_id=test_user.id,
        is_published=True
    )
    db_session.add(article)
    await db_session.commit()
    await db_session.refresh(article)
    result = await db_session.execute(
        select(Article)
        .options(joinedload(Article.author))
        .filter_by(id=article.id)
    )
    article = result.scalar_one()
    return article
