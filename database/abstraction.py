from typing import Iterator, Any 
from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker  # type: ignore
from sqlalchemy import create_engine  # type: ignore

from utils.config import DatabaseInfo

class Database:
    def __init__(self, db_info: DatabaseInfo) -> None:
        self.engine = create_engine(db_info.connection_string)
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

    @contextmanager
    def commit_only_session(self) -> Iterator[Any]:
        session = self.Session()
        yield session
        session.commit()
        
