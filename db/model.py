
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Dictionaly(Base):
    __tablename__ = 'dictionaly'

    id = Column(Integer, primary_key=True)
    kana = Column(String(255), nullable=False)
    length = Column(Integer, nullable=False)
