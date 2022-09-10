from flask import Blueprint, Response, json
from flask_pydantic import validate

from src.schema.logger import LoggerRequestSchema
from src.operators.logger import apply

logger = Blueprint("Logger", __name__)



@logger.get("/apply")
@validate()
def apply_endpoint(query: LoggerRequestSchema):
    return Response(
        json.dumps(apply(query.limit)),
        status=200,
        content_type="application_json")
