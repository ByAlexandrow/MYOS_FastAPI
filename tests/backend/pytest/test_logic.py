import pytest

from sqlalchemy import select

from app.models.category import Category
from app.models.article import Article, Carousel


@pytest.mark.asyncio
async def test_category_article_relationship(db_session, fixture_create_test_category, fixture_create_test_article):
    async with db_session as session:
        category = fixture_create_test_category
        article = fixture_create_test_article

        article.category_id = category.id

        session.add(article)
        await session.commit()

        result = await session.execute(
            select(Article).filter(Article.category_id == category.id)
        )
        articles = result.scalars().all()

        assert len(articles) == 1
        assert articles[0].title == article.title

        result = await session.execute(
            select(Category).join(Article).filter(Article.id == article.id)
        )
        loaded_category = result.scalar_one_or_none()

        assert article.category_id == category.id
        assert loaded_category is not None
        assert loaded_category.title == category.title


@pytest.mark.asyncio
async def test_article_carousel_relationship(db_session, fixture_create_test_article, fixture_create_test_carousel):
    async with db_session as session:
        article = fixture_create_test_article
        carousel = fixture_create_test_carousel

        carousel.article_id = article.id

        session.add(carousel)
        await session.commit()

        result = await session.execute(
            select(Carousel).filter(Carousel.article_id == article.id)
        )
        carousels = result.scalars().all()

        assert len(carousels) == 1
        assert carousels[0].title == carousel.title

        result = await session.execute(
            select(Article).join(Carousel).filter(Carousel.id == carousel.id)
        )
        loaded_article = result.scalar_one_or_none()

        assert carousel.article_id == article.id
        assert loaded_article is not None
        assert loaded_article.title == article.title
