from functools import wraps
from flask import request, json
from src.models.blacklist import BlackList

from flask import Response


def authorization(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            raise ValueError('Missing authorization header')

        token_schema, token = auth_header.split(' ')        
        valid_token_schemes = ['Bearer']

        if token_schema not in valid_token_schemes:
            return Response(
                json.dumps(
                    {
                        "success": False,
                        "message": "Not valid token schema"
                    }
                ),
                status=401,
                content_type='application/json'
            )
        
        if token is None or token == '':
            raise ValueError('Token not transfered')

        if BlackList.get_by_token(token) is not None:
            return Response(json.dumps(
                {
                    'success': False,
                    'message': 'Token in blacklist'
                }),
                status=401,
                content_type='application/json'
            )
        else:
            return func(token, *args, **kwargs)
    return wrapper
