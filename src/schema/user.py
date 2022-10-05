import uuid
import bcrypt
from typing import List, Optional
import enum

from pydantic import BaseModel, Field, validator

from src.schema.response import ResponseSchema
from src.models.user import RoleEnum


class UserSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    role: Optional[RoleEnum]
    username: str
    hash_password: str = Field(alias="password")

    @validator("hash_password", pre=True)
    def password_hasher(cls, value: str) -> bytes:
        if isinstance(value, str):
            return bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())
        elif isinstance(value, bytes):
            return value
        else:
            raise ValueError("Пароль должен быть передан строкой.")

    class Config:
        orm_mode = True
        validate_assignment = True
        allow_population_by_field_name = True


class LoginUserSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    username: str
    password: str = Field(alias="password")

    class Config:
        orm_mode = True
        validate_assignment = True
        allow_population_by_field_name = True


class UserSecureSchema(BaseModel):
    id: uuid.UUID
    role: RoleEnum
    username: str

    def __hash__(self):
        return hash((self.id, self.username, self.role))

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UsersSecureSchema(BaseModel):
    __root__: List[UserSecureSchema] = Field(alias="data")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True