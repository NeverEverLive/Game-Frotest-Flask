import logging
from typing import Union

from src.schema.company import CompanySchema
from src.schema.response import ResponseSchema
from src.schema.accomplices import AccomplicesSchema
from src.models.developer import Developer
from src.models.sponsor import Sponsor
from src.models.publisher import Publisher
from src.models.base_model import get_session



def create_accompile(data: CompanySchema, accompile_type: Union[Developer, Sponsor, Publisher], game_id) -> ResponseSchema:
    # accompile_state = accompile_type().fill(
    #     company_id=data.id,
    #     game_id=game_id
    # )

    # with get_session() as session:
    #     session.add(accompile_state)
    #     session.commit()

    return ResponseSchema(
        data=AccomplicesSchema.parse_obj(dict(company_id=data.id, game_id=game_id)),
        message="Article created successfuly",
        success=True
    )