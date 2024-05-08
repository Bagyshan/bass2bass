from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, async_scoped_session
from asyncio import current_task
from .config import settings


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'

    id: Mapped[int] = mapped_column(primary_key=True)

engine = create_async_engine(settings.DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession  
)

async def get_db():
    async with async_session_maker() as session:
        yield session
        await session.close()

def get_scoped_session():
    session = async_scoped_session(
        session_factory=async_session_maker,
        scopefunc=current_task,
    )
    return session

async def session_dependency() -> AsyncSession:  # type: ignore
    async with async_session_maker() as session:
        yield session
        await session.close()

async def scoped_session_dependency() -> AsyncSession:  # type: ignore
    session = get_scoped_session()
    yield session
    await session.close()