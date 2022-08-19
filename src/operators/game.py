

import logging
from src.models.base_model import get_session
from src.models.game import Game
from src.models.developer import Developer
from src.models.publisher import Publisher
from src.models.sponsor import Sponsor
from src.schema.game import GameSchema, GetGameSchema, GameCompanyRelationSchema
from src.schema.developer import DeveloperSchema
from src.schema.publisher import PublisherSchema
from src.schema.sponsor import SponsorSchema
from src.schema.response import ResponseSchema


def _create_developer(game, developer):
    developer.game_id = game.id
    developer_state = Developer().fill(**developer.dict())

    with get_session() as session:
        session.add(developer_state)
        session.commit()

        return developer_state


def _create_publisher(game, publisher):
    publisher.game_id = game.id
    publisher_state = Publisher().fill(**publisher.dict())

    with get_session() as session:
        session.add(publisher_state)
        session.commit()

        return publisher_state


def _create_sponsor(game, sponsor):
    sponsor.game_id = game.id
    sponsor_state = Sponsor().fill(**sponsor.dict())

    with get_session() as session:
        session.add(sponsor_state)
        session.commit()


def _create_accomplices(data):
    if data.developer:
        _create_developer(data.game, data.developer)
    if data.publisher:
        _create_publisher(data.game)
    if data.sponsor:
        _create_sponsor(data.game)


def create_game(data: GameCompanyRelationSchema) -> ResponseSchema:
    game_state = Game().fill(**data.game.dict())
    
    _create_accomplices(data)
    
    with get_session() as session:
        session.add(game_state)
        session.commit()
        
        return ResponseSchema(
            data=GameCompanyRelationSchema.from_orm(data),
            message="Game created successfuly",
            success=True
        )


def get_game(game: GetGameSchema) -> ResponseSchema:
    with get_session() as session:
        game_state = session.query(Game).filter_by(id=game.id).first()
        developer_state = session.query(Developer).filter_by(game_id=game.id).first()
        publisher_state = session.query(Publisher).filter_by(game_id=game.id).first()
        sponsor_state = session.query(Sponsor).filter_by(game_id=game.id).first()
        
        if not game_state:
            return ResponseSchema(
                success=False,
                message="Same game doesn't exist"
            )

        publisher = None
        sponsor = None
        game=GameSchema.from_orm(game_state)
        developer=DeveloperSchema.from_orm(developer_state)
        if publisher_state:
            publisher=PublisherSchema.from_orm(publisher_state)
        if sponsor_state:
            sponsor=SponsorSchema.from_orm(sponsor_state)

        data = {
            "game": game,
            "developer": developer,
            "publisher": publisher,
            "sponsor": sponsor
        }

        return ResponseSchema(
            data=GameCompanyRelationSchema.parse_obj(data),
            success=True
        )


# def update_genre(genre: GenreSchema) -> ResponseSchema:

#     genre_state = Genre().fill(**genre.dict())

#     with get_session() as session:
#         session.merge(genre_state)
#         session.commit()

#         return ResponseSchema(
#             data=GenreSchema.from_orm(genre_state),
#             message="Genre updated",
#             success=True
#         )


# def delete_genre(genre: GetGenreSchema) -> ResponseSchema:

#     with get_session() as session:
#         genre_state = session.query(Genre).filter_by(id=genre.id).first()

#         if not genre_state:
#             return ResponseSchema(
#                 success=False,
#                 message="Same genre doesn't exist"
#             )

#         session.delete(genre_state)
#         session.commit()

#         return ResponseSchema(
#             data=GenreSchema.from_orm(genre_state),
#             message="Genre deleted",
#             success=True
#         )

