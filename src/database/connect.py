from contextlib import AbstractContextManager, contextmanager
from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, scoped_session, sessionmaker

from config import DB_ISOLATION_LEVEL, DB_URL

class Base(DeclarativeBase):
    pass

engine = create_engine(DB_URL, echo=False, isolation_level=DB_ISOLATION_LEVEL)
session_factory = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
)

@contextmanager
def db_session() -> Callable[..., AbstractContextManager[Session]]:
    session: Session = session_factory()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
