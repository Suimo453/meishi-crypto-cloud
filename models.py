from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Float, BigInteger
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import DateTime
Base = declarative_base()
engine = create_engine(f'sqlite:///db.sqlite3')
SessionClass = sessionmaker(engine)
session = SessionClass()

class Meishi(Base):
    __tablename__ = 'meishi'
    company = Column(String(255))
    id = Column(Integer, primary_key=True)
    firstname = Column(String(255))
    lastname = Column(String(255))
    mail = Column(String(255))
    department = Column(String(255))
    picture = Column(String(50*1000*1000))
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

class MeishiKey(Base):
    __tablename__ = 'meishikey'
    id = Column(Integer, primary_key=True)
    company = Column(String(255))
    firstname = Column(String(255))
    lastname = Column(String(255))
    meishi_id = Column(Integer)


Base.metadata.create_all(engine)

if __name__ == "__main__":
    pass
