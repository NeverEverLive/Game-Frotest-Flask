from datetime import datetime
from typing import Optional
import uuid
from src.models.base_model import BaseModel

from sqlalchemy import Column, func, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import String, DateTime, LargeBinary
from pydantic import BaseModel as BaseSchema


class Image(BaseModel):
    __tablename__ = 'image'

    id = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4())
    file = Column(LargeBinary, nullable=False)
    name = Column(String, nullable=False) 
    mimetype = Column(String, nullable=False)
    inserted_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=datetime.now)

    game = relationship('Game', back_populates='image', uselist=False, cascade="all,delete")

    __table_args__ = (
        PrimaryKeyConstraint(id),
    )


class ImageSchema(BaseSchema):
    id: uuid.UUID
    file: str
    name: str
    mimetype: str
