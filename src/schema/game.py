import datetime
import uuid
from typing import List, Optional

from pydantic import BaseModel, Field, validator
from src.schema.accomplices import AccomplicesSchema


class GameSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: str
    description: Optional[str]
    date: datetime.date
    image_id: uuid.UUID
    genre_id: uuid.UUID

    def __hash__(self):
        return hash((
            self.id,
            self.title, 
            self.description, 
            self.date, 
            self.image_id, 
            self.genre_id
        ))

    @validator('date')
    def data_formatter(cls, value: str):
        if isinstance(value, str):
            value = datetime.datetime.strptime(value, '%d-%m-%Y')
        return str(value)

    class Config:
        orm_mode = True
    

class GamesSchema(BaseModel):
    __root__: List[GameSchema] = Field(alias="data")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class GetGameSchema(BaseModel):
    id: uuid.UUID


class GameCompanyRelationSchema(BaseModel):
    game: GameSchema
    developer: AccomplicesSchema
    publisher: Optional[AccomplicesSchema]
    sponsor: Optional[AccomplicesSchema]

    def __hash__(self):
        return hash((self.game, self.developer, self.publisher, self.sponsor))

    class Config:
        orm_mode = True
