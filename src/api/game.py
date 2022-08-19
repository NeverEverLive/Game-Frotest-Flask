import logging
from flask import Response, json, Blueprint
from flask_pydantic import validate

from src.api.utils import authorization
from src.schema.game import GetGameSchema, GameCompanyRelationSchema
from src.operators.game import create_game, get_game


game = Blueprint("game", __name__)


@game.post('/')
@validate()
@authorization
def create(token, body: GameCompanyRelationSchema):
    logging.warning(body)
    response = create_game(body)
    return Response(
        json.dumps(response),
        status=201,
        content_type='application/json'
    )


@game.get('/')
@validate()
@authorization
def get(token, body: GetGameSchema):
    response = get_game(body)
    return Response(
        json.dumps(response),
        status=200,
        content_type='application/json'
    )

# @genre.put('/')
# @validate()
# @authorization
# def update(token, body: GenreSchema):
#     response = update_genre(body)
#     return Response(
#         json.dumps(response),
#         status=200,
#         content_type='application/json'
#     )


# @genre.delete('/')
# @validate()
# @authorization
# def delete(token, body: GetGenreSchema):
#     response = delete_genre(body)
#     return Response(
#         json.dumps(response),
#         status=202,
#         content_type='application/json'
#     )
