import logging

from flask import Response, json, Blueprint, request
from flask_pydantic import validate

from src.api.utils import authorization
from src.schema.image import GetImageSchema
from src.operators.image import upload, get_image


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


@image.get('/')
@validate()
@authorization
def get(token, body: GetImageSchema):
    response, mimetype = get_image(body)
    logging.warning(mimetype)
    return Response(
        response,
        mimetype=mimetype
    )
