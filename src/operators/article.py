import logging

from src.models.base_model import get_session
from src.models.article import Article
from src.schema.article import ArticleSchema, ArticlesSchema
from src.schema.response import ResponseSchema, ManyResponseSchema


def create_article(article: ArticleSchema) -> ResponseSchema:
    article_state = Article().fill(**article.dict())

    logging.warning(ArticleSchema.from_orm(article_state))

    with get_session() as session:
        session.add(article_state)
        session.commit()
        return ResponseSchema(
            data=ArticleSchema.from_orm(article_state),
            message="Article created successfuly",
            success=True
        )


def get_article(id: str) -> ResponseSchema:
    with get_session() as session:
        article_state = session.query(Article).filter_by(id=id).first()

        if not article_state:
            return ResponseSchema(
                success=False,
                message="Same article doesn't exist"
            )

        return ResponseSchema(
            data=ArticleSchema.from_orm(article_state),
            success=True
        )


def get_all_article() -> ResponseSchema:
    with get_session() as session:
        article_state = session.query(Article).order_by(Article.inserted_at.desc()).all()

        data = ArticlesSchema.from_orm(article_state).dict(by_alias=True)["data"]

        return ResponseSchema(
            data=data,
            success=True
        )
