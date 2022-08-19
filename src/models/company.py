from datetime import datetime
from typing import Optional
import uuid
from src.models.base_model import BaseModel

from sqlalchemy import Column, func, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import String, DateTime
from pydantic import BaseModel as BaseSchema


class Company(BaseModel):
    __tablename__ = 'company'

    id = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4())
    name = Column(String, nullable=False)
    description = Column(String)
    inserted_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=datetime.now)

    developer = relationship('Developer', back_populates='company', uselist=True, cascade="all,delete-orphan")
    publisher = relationship('Publisher', back_populates='company', uselist=True, cascade="all,delete-orphan")
    sponsor = relationship('Sponsor', back_populates='company', uselist=True, cascade="all,delete-orphan")

    __table_args__ = (
        PrimaryKeyConstraint(id),
    )


class CompanySchema(BaseSchema):
    id: uuid.UUID
    name: str
    description: Optional[str]
