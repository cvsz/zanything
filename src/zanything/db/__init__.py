"""Durable Data Runtime: Async database engine, session management, and Base models."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from zanything.config import get_settings
from zanything.logging import get_logger

logger = get_logger("zanything.db")


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy declarative models."""

    pass


class DatabaseSessionManager:
    """Manages async database engine and scoped session lifecycle."""

    def __init__(self) -> None:
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker[AsyncSession] | None = None

    def init_engine(self, database_url: str | None = None, echo: bool = False) -> None:
        """Initialize the async database engine."""
        settings = get_settings()
        url = database_url or settings.database_url

        # Configure engine options based on dialect
        connect_args: dict[str, Any] = {}
        if url.startswith("sqlite"):
            connect_args["check_same_thread"] = False

        self._engine = create_async_engine(
            url,
            echo=echo,
            connect_args=connect_args,
            pool_pre_ping=True,
        )
        self._sessionmaker = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )
        logger.info(f"Database engine initialized for {url.split('@')[-1]}")

    async def close(self) -> None:
        """Close database engine connection pool."""
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._sessionmaker = None
            logger.info("Database engine connections closed")

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """Provide an isolated transactional async database session."""
        if self._sessionmaker is None:
            raise RuntimeError("Database session maker failed to initialize.")
        session: AsyncSession = self._sessionmaker()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Global database session manager singleton
db_manager = DatabaseSessionManager()


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency yielding an async database session."""
    async with db_manager.session() as session:
        yield session
