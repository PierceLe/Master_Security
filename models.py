'''
models
defines sql alchemy data models
also contains the definition for the room class used to keep track of socket.io rooms

Just a sidenote, using SQLAlchemy is a pain. If you want to go above and beyond,
do this whole project in Node.js + Express and use Prisma instead,
Prisma docs also looks so much better in comparison

or use SQLite, if you're not into fancy ORMs (but be mindful of Injection attacks :) )
'''

from sqlalchemy import ForeignKey, Integer, String, TIME, DateTime, Boolean, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List


# data models
class Base(DeclarativeBase):
    pass


class Relationships(Base):
    __tablename__ = 'relationships'
    relationship_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('users.user_id'))
    friend_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('users.user_id'))
    status: Mapped[Integer] = mapped_column(Integer)


class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fullname: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String, unique=True)
    avatar: Mapped[str] = mapped_column(String)
    pb_key: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    salt: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)
    online: Mapped[bool] = mapped_column(Boolean, default=False)
    time_created: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    time_updated: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    relationships: Mapped[List["Relationships"]] = relationship(foreign_keys="[Relationships.user_id]")


class Message(Base):
    __tablename__ = "messages"
    message_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kind: Mapped[str] = mapped_column(String, default="text")
    content: Mapped[str] = mapped_column(String)
    author: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))
    room_id: Mapped[int] = mapped_column(Integer, ForeignKey('rooms.room_id'))
    time_created: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    time_updated: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class Comment(Base):
    __tablename__ = "comments"
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    article_id: Mapped[str] = mapped_column(Integer, ForeignKey('articles.article_id'))
    content: Mapped[str] = mapped_column(String)
    author: Mapped[str] = mapped_column(Integer, ForeignKey('users.user_id'))
    time_created: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    time_updated: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class Article(Base):
    __tablename__ = "articles"
    article_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String)
    author: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))
    time_created: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    time_updated: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class UserRoom(Base):
    __tablename__ = "user_rooms"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(Integer, ForeignKey('users.user_id'))
    room_id: Mapped[str] = mapped_column(Integer, ForeignKey('rooms.room_id'))
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)


class Room(Base):
    __tablename__ = "rooms"
    room_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    room_name: Mapped[str] = mapped_column(String)
    room_img: Mapped[str] = mapped_column(String)
    room_type: Mapped[str] = mapped_column(String, default="single")
    room_master: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=True)
    time_created: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    time_updated: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class Block(Base):
    __tablename__ = "blocks"
    block_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type_block: Mapped[str] = mapped_column(String)
    user_block: Mapped[str] = mapped_column(Integer, ForeignKey('users.user_id'))
    time_created: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    time_updated: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
