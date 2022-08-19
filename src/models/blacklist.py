from src.models.base_model import BaseModel
from sqlalchemy import Column, PrimaryKeyConstraint, types, func
from marshmallow import Schema, fields


class BlackList(BaseModel):
    __tablename__ = 'blacklist'

    id = Column(types.String, nullable=False)
    token = Column(types.String, unique=True, nullable=False)
    blacklisted_on = Column(types.DateTime, nullable=False, server_default=func.now())
    
    __table_args__ = (
        PrimaryKeyConstraint(id),
    )

    @classmethod
    def get_by_token(cls, token):
        return cls.query.filter_by(token=token).first()


class BlackListSchema(Schema):
    id = fields.UUID()
    token = fields.String()
