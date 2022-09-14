from typing import List, Optional
from pydantic import BaseModel, Field, validator
import uuid


class CompanySchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    description: Optional[str]

    def __hash__(self):
        return hash((self.id, self.name, self.description))

    @validator("id")
    def uuid_to_str(cls, value: uuid.UUID):
        if isinstance(value, uuid.UUID):
            return str(value)

    class Config:
        orm_mode = True
    

class CompaniesSchema(BaseModel):
    __root__: List[CompanySchema] = Field(alias="data")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class GetCompanySchema(BaseModel):
    id: uuid.UUID
