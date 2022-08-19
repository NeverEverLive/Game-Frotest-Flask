from datetime import datetime
from typing import Optional
import uuid
from src.models.base_model import BaseModel

from sqlalchemy import Column, func, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import String, DateTime
from pydantic import BaseModel as BaseSchema


class Genre(BaseModel):
    __tablename__ = 'genre'

    id = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4())
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    inserted_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=datetime.now)

    game = relationship('Game', back_populates='genre', uselist=False)

    __table_args__ = (
        PrimaryKeyConstraint(id),
    )


class GenreSchema(BaseSchema):
    id: uuid.UUID
    name: str
    description: Optional[str]
