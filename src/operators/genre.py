

import logging
from src.models.base_model import get_session
from src.models.genre import Genre
from src.schema.genre import GenreSchema, GetGenreSchema
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


def get_genre(genre: GetGenreSchema) -> ResponseSchema:
    with get_session() as session:
        genre_state = session.query(Genre).filter_by(id=genre.id).first()

        if not genre_state:
            return ResponseSchema(
                success=False,
                message="Same genre doesn't exist"
            )

        return ResponseSchema(
            data=GenreSchema.from_orm(genre_state),
            success=True
        )


def update_genre(genre: GenreSchema) -> ResponseSchema:

    user_state = Genre().fill(**genre.dict())

    with get_session() as session:
        session.merge(user_state)
        session.commit()

        return ResponseSchema(
            data=GenreSchema.from_orm(user_state),
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

