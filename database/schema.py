from typing import Any

from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy import Column, Integer, Text, DateTime  # type: ignore

Base = declarative_base()  # type: Any

class Submission(Base):
    __tablename__ = 'Submission'

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    author = Column(Text)
    created_utc = Column(DateTime)
    fullname = Column(Text)
    body_markdown = Column(Text)
    body_html = Column(Text)
    url = Column(Text)

class Comment(Base):
    __tablename__ = 'Comment'

    id = Column(Integer, primary_key=True)
    author = Column(Text)
    created_utc = Column(DateTime)
    fullname = Column(Text)
    body_markdown = Column(Text)
    body_html = Column(Text)
    url = Column(Text)
    parent = Column(Text)

