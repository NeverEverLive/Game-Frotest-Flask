from flask import Blueprint, jsonify, request, json, Response

from src.operators.user import create_user, get_user, login_user, logout_user, update_user
from src.api.utils import authorization


account = Blueprint('api', __name__)


@account.post('/user')
def create_user_endpoint():
    response = create_user(request.get_json())
    return Response(
        json.dumps(response),
        status=201,
        content_type='application/json'
    )


@account.get('user/<username>')
def get_user_endpoint(username):
    response = get_user(username)
    return Response(
        json.dumps(response),
        status=200,
        content_type='application/json'
    )

@account.put('/user')
@authorization
def update_user_endpoint(token):
    print(token)
    response = update_user(request.get_json(), token)
    return Response(
        json.dumps(response),
        status=200,
        content_type='application/json'
    )

@account.post('/user/login')
def login_user_endpoint():
    response = login_user(request.get_json())
    print(response)
    return Response(
        json.dumps(response),
        status=200,
        content_type='application/json'
    )


@account.post('/user/logout')
@authorization
def logout_user_endpoint(token):
    response = logout_user(token)
    print(response)
    return Response(
        json.dumps(response),
        status=200,
        content_type='application/json'
    )
