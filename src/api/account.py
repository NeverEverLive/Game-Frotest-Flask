from flask import Blueprint, jsonify, request, json, Response

from src.operators.user import create_user, get_user, login, update_user
from src.api.utils import authorization


account = Blueprint('api', __name__)


@account.post('/')
def create():
    response = create_user(request.get_json())
    return Response(
        json.dumps(response),
        status=201,
        content_type='application/json'
    )


@account.get('/<string:username>')
def get(username):
    response = get_user(username)
    return Response(
        json.dumps(response),
        status=200,
        content_type='application/json'
    )

@account.put('/')
@authorization
def update(token):
    print(token)
    response = update_user(request.get_json(), token)
    return Response(
        json.dumps(response),
        status=200,
        content_type='application/json'
    )

@account.post('/login')
def login():
    response = login_user(request.get_json())
    print(response)
    return Response(
        json.dumps(response),
        status=200,
        content_type='application/json'
    )
