from datetime import datetime
from uuid import uuid4
from src.models.base_model import BaseModel

from sqlalchemy import Column, func, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import String, DateTime
from marshmallow import Schema, fields


class User(BaseModel):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid4())
    username = Column(String, unique=True, nullable=False)
    hash_password = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=datetime.now)
    
    article = relationship("Article", back_populates="user", uselist=True, cascade="all,delete")

    __table_args__ = (
        PrimaryKeyConstraint(id),
    )

    def __repr__(self):
        return self.email

    @classmethod
    def get_by_id(cls, id):
        """Вернуть пользователя по id"""
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_username(cls, username):
        """Вернуть пользователя по email"""
        return cls.query.filter_by(username=username).first()


class LoginUserSchema(Schema):
    username = fields.String()
    password = fields.String()


class CreateUpdateUserSchema(Schema):
    id = fields.UUID()
    username = fields.Email()
    hash_password = fields.String()
