

import logging
from src.models.base_model import get_session
from src.models.genre import Genre
from src.schema.genre import GenreSchema, GenresSchema, GetGenreSchema
from src.schema.response import ResponseSchema


def create_genre(genre: GenreSchema) -> ResponseSchema:
    genre_state = Genre().fill(**genre.dict())

    logging.warning(GenreSchema.from_orm(genre_state))

    with get_session() as session:
        session.add(genre_state)
        session.commit()
        
        return ResponseSchema(
            data=GenreSchema.from_orm(genre_state),
            message="Genre created successfuly",
            success=True
        )


def get_genre(id: str) -> ResponseSchema:
    with get_session() as session:
        genre_state = session.query(Genre).filter_by(id=id).first()

        if not genre_state:
            return ResponseSchema(
                success=False,
                message="Same genre doesn't exist"
            )

        return ResponseSchema(
            data=GenreSchema.from_orm(genre_state),
            success=True
        )

def get_genre_by_title(title: str) -> ResponseSchema:
    with get_session() as session:
        genre_state = session.query(Genre).filter_by(title=title).first()

        if not genre_state:
            return ResponseSchema(
                success=False,
                message="Same genre doesn't exist"
            )

        return ResponseSchema(
            data=GenreSchema.from_orm(genre_state),
            success=True
        )

def get_all_genries() -> ResponseSchema:
    with get_session() as session:
        article_state = session.query(Genre).order_by(Genre.inserted_at.desc()).all()

        data = GenresSchema.from_orm(article_state).dict(by_alias=True)["data"]

        return ResponseSchema(
            data=data,
            success=True
        )


def update_genre(genre: GenreSchema) -> ResponseSchema:

    genre_state = Genre().fill(**genre.dict())

    with get_session() as session:
        session.merge(genre_state)
        session.commit()

        return ResponseSchema(
            data=GenreSchema.from_orm(genre_state),
            message="Genre updated",
            success=True
        )


def delete_genre(genre: GetGenreSchema) -> ResponseSchema:

    with get_session() as session:
        genre_state = session.query(Genre).filter_by(id=genre.id).first()

        if not genre_state:
            return ResponseSchema(
                success=False,
                message="Same genre doesn't exist"
            )

        session.delete(genre_state)
        session.commit()

        return ResponseSchema(
            data=GenreSchema.from_orm(genre_state),
            message="Genre deleted",
            success=True
        )

