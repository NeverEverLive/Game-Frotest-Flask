import logging

from src.models.base_model import get_session
from src.models.company import Company
from src.schema.company import CompanySchema, GetCompanySchema
from src.schema.response import ResponseSchema


def create_company(company: CompanySchema) -> ResponseSchema:
    company_state = Company().fill(**company.dict())

    logging.warning(CompanySchema.from_orm(company_state))

    with get_session() as session:
        session.add(company_state)
        session.commit()
        return ResponseSchema(
            data=CompanySchema.from_orm(company_state),
            message="Company created successfuly",
            success=True
        )


def get_company(company: GetCompanySchema) -> ResponseSchema:
    with get_session() as session:
        company_state = session.query(Company).filter_by(id=company.id).first()

        if not company_state:
            return ResponseSchema(
                success=False,
                message="Same company doesn't exist"
            )

        return ResponseSchema(
            data=CompanySchema.from_orm(company_state),
            success=True
        )


def update_company(company: CompanySchema) -> ResponseSchema:

    company_state = Company().fill(**company.dict())

    with get_session() as session:
        session.merge(company_state)
        session.commit()

        return ResponseSchema(
            data=CompanySchema.from_orm(company_state),
            message="Company updated",
            success=True
        )


def delete_company(company: GetCompanySchema) -> ResponseSchema:

    with get_session() as session:
        company_state = session.query(Company).filter_by(id=company.id).first()

        if not company_state:
            return ResponseSchema(
                success=False,
                message="Same company doesn't exist"
            )

        session.delete(company_state)
        session.commit()

        return ResponseSchema(
            data=CompanySchema.from_orm(company_state),
            message="Company deleted",
            success=True
        )

