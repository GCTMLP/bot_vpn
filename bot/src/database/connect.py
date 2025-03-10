from contextlib import AbstractContextManager, contextmanager
from typing import Callable
import logging
from logging.config import dictConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    scoped_session,
    sessionmaker
)

from src.config import (
    DB_ISOLATION_LEVEL,
    DB_URL,
    LOGGING_CONFIG
)

ERROR_LOG = logging.getLogger("error")
dictConfig(LOGGING_CONFIG)


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
    except Exception as e:
        session.rollback()
        ERROR_LOG.error(f'ERROR in create db_session {str(e)}')
    finally:
        session.close()
