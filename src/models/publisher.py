from datetime import datetime
from typing import Optional
import uuid
from src.models.base_model import BaseModel

from sqlalchemy import Column, func, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import DateTime
from pydantic import BaseModel as BaseSchema


class Publisher(BaseModel):
    __tablename__ = 'publisher'

    id = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4())
    game_id = Column(UUID(as_uuid=True), nullable=False)
    company_id = Column(UUID(as_uuid=True), nullable=False)
    inserted_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=datetime.now)

    company = relationship('Company', back_populates='publisher', uselist=False, cascade="all,delete")
    game = relationship('Game', back_populates='publisher', uselist=True)

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
                company_id,
            ),
            (
                "company.id",
            )
        )
    )


class PublisherSchema(BaseSchema):
    id: uuid.UUID
    game_id: uuid.UUID
    company_id: uuid.UUID
