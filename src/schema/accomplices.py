from typing import Optional
import uuid

from pydantic import BaseModel, Field, validator


class AccomplicesSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    company_id: uuid.UUID
    game_id: Optional[uuid.UUID]

    def __hash__(self):
        return hash((self.id, self.company_id, self.game_id))

    @validator("id", "company_id", "game_id")
    def uuid_to_str(cls, value: uuid.UUID):
        if isinstance(value, uuid.UUID):
            return str(value)

    class Config:
        orm_mode = True
