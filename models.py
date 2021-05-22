import datetime
import hashlib

from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship

from db_engine import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, )
    username = Column(String(32), nullable=False)
    _password = Column("password", String(200), nullable=False)
    create_time = Column(DateTime, default=datetime.datetime.utcnow)
    todos = relationship("ToDo", back_populates='users')

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value: str):
        self._password = self.hash_password(value)

    @classmethod
    def hash_password(cls, value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()


class ToDo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, )
    user_name = Column(Integer, ForeignKey(User.username), nullable=False)
    text = Column(Text, nullable=False)
    status = Column(String(10))
    create_time = Column(DateTime, default=datetime.datetime.utcnow)
    update_time = Column(DateTime, default=datetime.datetime.utcnow)
    users = relationship(User, back_populates='todos')

    def __init__(self, text: str, user_name: str, status: str):
        self.user_name = user_name
        self.text = text
        self.status = status
