from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from src.config import get_settings

engine = create_engine(get_settings().DATABASE_URL, echo=True)


def init_db() -> None:
    """Create all tables defined by SQLModel metadata."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session."""
    with Session(engine) as session:
        yield session
