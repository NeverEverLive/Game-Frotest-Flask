import logging
from flask import Response, json, Blueprint
from flask_pydantic import validate

from src.api.utils import authorization
from src.schema.game import GetGameSchema, GameCompanyRelationSchema
from src.operators.game import create_game, delete_game, get_game, get_all_game, update_game


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


@game.get('/<string:id>')
@authorization
def get(token, id):
    response = get_game(id)
    return Response(
        json.dumps(response),
        status=200,
        content_type='application/json'
    )


@game.get("/")
@authorization
def get_all(token):
    response = get_all_game()
    return Response(
        json.dumps(response),
        status=200,
        content_type="application/json"
    )

@game.put('/')
@validate()
@authorization
def update(token, body: GameCompanyRelationSchema):
    response = update_game(body)
    return Response(
        json.dumps(response),
        status=200,
        content_type='application/json'
    )


@game.delete('/')
@validate()
@authorization
def delete(token, body: GetGameSchema):
    response = delete_game(body.id)
    return Response(
        json.dumps(response),
        status=202,
        content_type='application/json'
    )
