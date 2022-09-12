import logging
import uuid

from flask import json

from src.models.logger import Logger
from src.models.base_model import get_session
from src.models.article import Article
from src.schema.article import ArticleSchema, ArticlesSchema, GetArticleSchema
from src.schema.response import ResponseSchema


def create_article(article: ArticleSchema) -> ResponseSchema:
    article_state = Article().fill(**article.dict())

    logging.warning(ArticleSchema.from_orm(article_state))

    with get_session() as session:
        session.add(article_state)
        session.commit()

        logger_data = {
            "id": uuid.uuid4(),
            "table": "article",
            "action": "delete",
            "object_info": ArticleSchema.from_orm(article_state).dict()
        }

        logger_state = Logger().fill(**logger_data)
        session.add(logger_state)
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


def update_article(article: GetArticleSchema) -> ResponseSchema:
    with get_session() as session:
        logging.warning(session.query(Article).filter_by(id=article.id).first().title)
        logger_data = {
            "id": uuid.uuid4(),
            "table": "article",
            "action": "update",
            "object_info": ArticleSchema.from_orm(session.query(Article).filter_by(id=article.id).first()).dict()
        }
        
        article_state = Article().fill(**article.dict())

        session.merge(article_state)
        session.commit()

        logger_state = Logger().fill(**logger_data)
        session.add(logger_state)
        session.commit()

        return ResponseSchema(
                data=ArticleSchema.from_orm(article_state),
                message="Article updated successfuly",
                success=True
            )


def delete_article(article: GetArticleSchema) -> ResponseSchema:
    with get_session() as session:
        article_state = session.query(Article).filter_by(id=article.id).first()

        if not article_state:
            return ResponseSchema(
                success=False,
                message="Same article doesn't exist"
            )

        session.delete(article_state)
        session.commit()

        logger_data = {
            "id": uuid.uuid4(),
            "table": "article",
            "action": "insert",
            "object_info": ArticleSchema.from_orm(article_state).dict()
        }

        logger_state = Logger().fill(**logger_data)
        session.add(logger_state)
        session.commit()
    
        return ResponseSchema(
                data=ArticleSchema.from_orm(article_state),
                message="Article deleted successfuly",
                success=True
            )
