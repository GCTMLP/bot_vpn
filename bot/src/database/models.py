import enum
from datetime import datetime
from sqlalchemy import (
    JSON,
    TEXT,
    TIMESTAMP,
    UUID,
    Boolean,
    Column,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    DateTime
)
from sqlalchemy.orm import relationship

from src.database.connect import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    crated_at = Column(DateTime, default=datetime.utcnow)
    
    key = relationship("Keys", back_populates="user", lazy="selectin")
    payment = relationship("Payments", back_populates="user", lazy="selectin")
    

class Keys(Base):
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True)
    key_name = Column(String, nullable=False)
    user_id = Column(
        Integer,
        ForeignKey(
            "users.id", name="users_id_fkey", ondelete="CASCADE"
        ),
        nullable=True,
    )
    crated_at = Column(DateTime, default=datetime.utcnow)
    expire_at = Column(DateTime)
    
    user = relationship("Users", back_populates="key", lazy="selectin")


class Payments(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    sum = Column(Integer)
    user_id = Column(
        Integer,
        ForeignKey(
            "users.id", name="users_id_fkey", ondelete="CASCADE"
        ),
        nullable=True,
    )
    
    user = relationship("Users", back_populates="payment", lazy="selectin")
