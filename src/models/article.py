from datetime import datetime
from typing import Optional
import uuid
from src.models.base_model import BaseModel

from sqlalchemy import Column, func, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import String, DateTime, Boolean
from pydantic import Field, BaseModel as BaseSchema


class Article(BaseModel):
    __tablename__ = 'article'

    id = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4())
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    date = Column(DateTime, nullable=False, default=func.now())
    is_published = Column(Boolean, nullable=False, default=False)
    game_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    inserted_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=datetime.now)

    game = relationship('Game', back_populates='game', uselist=False, cascade="all,delete")
    user = relationship('User', back_populates='user', uselist=False, cascade="all,delete")


    __table_args__ = (
        PrimaryKeyConstraint(id),
        ForeignKeyConstraint(
            (
                game_id,
            ),
            (
                "game.id",
            )
        ),
        ForeignKeyConstraint(
            (
                user_id,
            ),
            (
                "user.id",
            )
        )
    )


class ArticleSchema(BaseSchema):
    id: uuid.UUID
    title: str
    description: Optional[str]
    date: datetime
    is_published: bool = Field(default=False)
    game_id: uuid.UUID
    user_id: uuid.UUID
