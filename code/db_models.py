from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String)
    image_url = Column(String)
    is_admin = Column(Boolean)
class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer)
    title = Column(String)
    post_text = Column(String)