from typing import Optional
from pydantic import BaseModel, Field
import uuid

class GenreSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: str
    description: Optional[str]

    def __hash__(self):
        return hash((self.id, self.title, self.description))

    class Config:
        orm_mode = True
    

class GetGenreSchema(BaseModel):
    id: uuid.UUID
