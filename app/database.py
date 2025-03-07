from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = 'sqlite+aiosqlite:///./myos.db'

enging = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = enging,
    class_ = AsyncSession
)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
