import logging
from flask import Response, json, Blueprint
from flask_pydantic import validate

from src.api.utils import authorization
from src.schema.article import ArticleSchema
from src.operators.article import create_article, get_all_article, get_article


article = Blueprint("article", __name__)


@article.post('/')
@validate()
@authorization
def create(token, body: ArticleSchema):
    response = create_article(body)
    return Response(
        json.dumps(response),
        status=201,
        content_type='application/json'
    )

@article.get('/<string:id>')
@authorization
def get(token, id):
    response = get_article(id)
    return Response(
        json.dumps(response),
        status=200,
        content_type='application/json'
    )


@article.get('/')
@authorization
def get_all(token):
    response = get_all_article()
    return Response(
        json.dumps(response),
        status=200,
        content_type='application/json'
    )
