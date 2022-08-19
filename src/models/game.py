from datetime import datetime
from typing import Optional
import uuid
from src.models.base_model import BaseModel

from sqlalchemy import Column, func, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import String, DateTime
from pydantic import BaseModel as BaseSchema


class Game(BaseModel):
    __tablename__ = 'game'

    id = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4())
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    date = Column(DateTime, nullable=False, default=func.now())
    image_id = Column(UUID(as_uuid=True), nullable=True)
    genre_id = Column(UUID(as_uuid=True), nullable=False)
    inserted_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=datetime.now)

    image = relationship('Image', back_populates='game', uselist=False, cascade="all,delete")
    genre = relationship('Genre', back_populates='game', uselist=False, cascade="all,delete")
    article = relationship("Article", back_populates="game", uselist=True, cascade="all,delete-orphan")
    developer = relationship('Developer', back_populates='game', uselist=False)
    publisher = relationship('Publisher', back_populates='game', uselist=False)
    sponsor = relationship('Sponsor', back_populates='game', uselist=False)


    __table_args__ = (
        PrimaryKeyConstraint(id),
        ForeignKeyConstraint(
            (
                image_id,
            ),
            (
                "image.id",
            )
        ),
        ForeignKeyConstraint(
            (
                genre_id,
            ),
            (
                "genre.id",
            )
        )
    )


class GameSchema(BaseSchema):
    id: uuid.UUID
    title: str
    description: Optional[str]
    date: datetime
    image_id: uuid.UUID
    genre_id: uuid.UUID
