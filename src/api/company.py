import logging
from flask import Response, json, Blueprint
from flask_pydantic import validate

from src.api.utils import authorization
from src.schema.company import CompanySchema, GetCompanySchema
from src.operators.company import create_company, get_all_companies, update_company, delete_company, get_company


company = Blueprint("company", __name__)


@company.post('/')
@validate()
@authorization
def create(token, body: CompanySchema):
    response = create_company(body)
    return Response(
        json.dumps(response),
        status=201,
        content_type='application/json'
    )


@company.get('/')
@validate()
@authorization
def get(token, body: GetCompanySchema):
    response = get_company(body)
    return Response(
        json.dumps(response),
        status=200,
        content_type='application/json'
    )

@company.put('/')
@validate()
@authorization
def update(token, body: CompanySchema):
    response = update_company(body)
    return Response(
        json.dumps(response),
        status=200,
        content_type='application/json'
    )


@company.delete('/')
@validate()
@authorization
def delete(token, body: GetCompanySchema):
    response = delete_company(body)
    return Response(
        json.dumps(response),
        status=202,
        content_type='application/json'
    )

@company.get("/all")
@authorization
def get_all(token):
    response = get_all_companies()
    return Response(
        json.dumps(response),
        status=200,
        content_type="application/json"
    )
