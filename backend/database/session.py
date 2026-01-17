from sqlmodel import create_engine, Session
from typing import Generator
from .config import settings
from contextlib import contextmanager

# Create the database engine
engine = create_engine( 
    settings.database_url,
    echo=settings.db_echo_sql,
    pool_pre_ping=True,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


# Alias for compatibility
get_db_session = get_session

@contextmanager
def get_session_context():
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

def create_tables():
    """Create all tables in the database - automatic table creation for hackathon"""
    from models.task import Task
    from models.user import User
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)

def init_db():
    """Initialize the database - for hackathon automatic setup"""
    create_tables()