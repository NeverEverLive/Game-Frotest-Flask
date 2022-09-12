import datetime
import uuid
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class ArticleSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: str
    description: Optional[str]
    date: datetime.date = Field(default_factory=datetime.date.today)
    is_published: bool = Field(default=False)
    game_id: uuid.UUID
    user_id: uuid.UUID

    def __hash__(self):
        return hash((
            self.id,
            self.title, 
            self.description, 
            self.date, 
            self.is_published, 
            self.game_id, 
            self.user_id
        ))

    @validator("id", "game_id", "user_id")
    def uuid_to_str(cls, value: uuid.UUID):
        if isinstance(value, uuid.UUID):
            return str(value)

    @validator('date')
    def data_formatter(cls, value: str):
        if isinstance(value, str):
            value = datetime.datetime.strptime(value, '%d-%m-%Y')
        return str(value)

    class Config:
        orm_mode = True
    

class ArticlesSchema(BaseModel):
    __root__: List[ArticleSchema] = Field(alias="data")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class GetArticleSchema(BaseModel):
    id: uuid.UUID