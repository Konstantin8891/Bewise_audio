import uuid

from sqlalchemy import Integer, Date, Text, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    name = Column(String, nullable=False)


class Audio(Base):
    __tablename__ = 'audio'
    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
        index=True
    )
    name = Column(String, nullable=False)
    user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    user = relationship('User', backref='audios')
