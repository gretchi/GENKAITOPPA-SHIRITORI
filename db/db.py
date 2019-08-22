
import sqlite3

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from .model import Base

class Database(object):
    def __init__(self, path, echo=False):
        engine = create_engine(f'sqlite:///{path}', echo=echo)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self._session = Session()

    @property
    def session(self):
        return self._session

    def close(self):
        self._session.close()
