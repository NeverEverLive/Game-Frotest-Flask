from typing import Optional
from pydantic import BaseModel, Field
import uuid


class ImageSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    file: bytes
    name: str
    mimetype: str

    def __hash__(self):
        return hash((self.id, self.file, self.name, self.mimetype))

    class Config:
        orm_mode = True
    

class GetImageSchema(BaseModel):
    id: uuid.UUID
