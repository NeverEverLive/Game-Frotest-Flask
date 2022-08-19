import logging
from werkzeug.utils import secure_filename

from flask import Response, json, Blueprint, request
from flask_pydantic import validate

from src.api.utils import authorization
from src.schema.image import ImageSchema
from src.operators.image import upload


image = Blueprint("image", __name__)


@image.post('/')
@authorization
def create(token):
    response = upload(request.files["file"])
    return Response(
        json.dumps(response),
        status=201,
        content_type='application/json'
    )


# @genre.get('/')
# @validate()
# @authorization
# def get(token, body: GetGenreSchema):
#     response = get_genre(body)
#     return Response(
#         json.dumps(response),
#         status=200,
#         content_type='application/json'
#     )

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
