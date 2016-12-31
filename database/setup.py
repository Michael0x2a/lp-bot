from typing import NewType, Any

from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.engine.base import Engine  # type: ignore

from database.schema import Base 


def make_test_engine() -> Engine:
    return create_engine('sqlite:///testdb.db', echo=True)

def create_database_tables(engine: Engine) -> None:
    Base.metadata.create_all(engine)

