from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from app.config import SQLITE_URL

engine = create_engine(SQLITE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(SessionLocal)

Base = declarative_base()


def initiate_db():
    Base.metadata.create_all(bind=engine)
