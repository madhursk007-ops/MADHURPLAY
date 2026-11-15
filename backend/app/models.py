from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user", nullable=False)

class WatchlistItem(Base):
    __tablename__ = "watchlist_items"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    poster_path = Column(String(255), nullable=True)
    __table_args__ = (UniqueConstraint("user_id", "movie_id"),)
