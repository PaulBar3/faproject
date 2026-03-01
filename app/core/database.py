from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# Асинхронный движок SQLAlchemy
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Логирование SQL-запросов
    pool_pre_ping=True,
)

# Фабрика сессий
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# Базовый класс для моделей
class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    """Зависимость для получения сессии БД."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Инициализация БД - создание таблиц."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
