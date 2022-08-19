import logging
from flask import Response, json, Blueprint
from flask_pydantic import validate

from src.api.utils import authorization
from src.schema.genre import GenreSchema, GetGenreSchema
from src.operators.genre import create_genre, update_genre, delete_genre, get_genre


genre = Blueprint("genre", __name__)


@genre.post('/')
@validate()
@authorization
def create(token, body: GenreSchema):
    response = create_genre(body)
    return Response(
        json.dumps(response),
        status=201,
        content_type='application/json'
    )


@genre.get('/')
@validate()
@authorization
def get(token, body: GetGenreSchema):
    response = get_genre(body)
    return Response(
        json.dumps(response),
        status=200,
        content_type='application/json'
    )

@genre.put('/')
@validate()
@authorization
def update(token, body: GenreSchema):
    response = update_genre(body)
    return Response(
        json.dumps(response),
        status=200,
        content_type='application/json'
    )


@genre.delete('/')
@validate()
@authorization
def delete(token, body: GetGenreSchema):
    response = delete_genre(body)
    return Response(
        json.dumps(response),
        status=202,
        content_type='application/json'
    )
