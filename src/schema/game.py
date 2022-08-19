import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, Field, validator

from src.schema.developer import DeveloperSchema
from src.schema.publisher import PublisherSchema
from src.schema.sponsor import SponsorSchema


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

    @validator('date', pre=True)
    def data_formatter(cls, value: str):
        if isinstance(value, str):
            value = datetime.datetime.strptime(value, '%d-%m-%Y')
        return value

    class Config:
        orm_mode = True
    

class GetGameSchema(BaseModel):
    id: uuid.UUID



class GameCompanyRelationSchema(BaseModel):
    game: GameSchema
    developer: DeveloperSchema
    publisher: Optional[PublisherSchema]
    sponsor: Optional[SponsorSchema]

    def __hash__(self):
        return hash((self.game, self.developer, self.publisher, self.sponsor))

    class Config:
        orm_mode = True
