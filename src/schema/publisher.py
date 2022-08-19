from typing import Optional
import uuid

from pydantic import BaseModel, Field


class PublisherSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    company_id: uuid.UUID
    game_id: Optional[uuid.UUID]

    def __hash__(self):
        return hash((self.id, self.company_id, self.game_id))

    class Config:
        orm_mode = True
