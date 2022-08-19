from typing import Optional
from pydantic import BaseModel, Field
import uuid


class CompanySchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    description: Optional[str]

    def __hash__(self):
        return hash((self.id, self.name, self.description))

    class Config:
        orm_mode = True
    

class GetCompanySchema(BaseModel):
    id: uuid.UUID
