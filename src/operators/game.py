

import logging
from src.operators.image import upload
from src.models.genre import Genre
from src.schema.company import CompanySchema
from src.schema.genre import GenreSchema
from src.models.base_model import get_session
from src.models.game import Game
from src.models.developer import Developer
from src.models.publisher import Publisher
from src.models.sponsor import Sponsor
from src.schema.game import GameSchema, GamesSchema, GetGameSchema, GameCompanyRelationSchema
from src.schema.accomplices import AccomplicesSchema
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
        _create_publisher(data.game, data.publisher)
    if data.sponsor:
        _create_sponsor(data.game, data.publisher)


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


def get_game(id: str) -> ResponseSchema:
    with get_session() as session:
        game_state = session.query(Game).filter_by(id=id).first()
        developer_state = session.query(Developer).filter_by(game_id=id).first()
        publisher_state = session.query(Publisher).filter_by(game_id=id).first()
        sponsor_state = session.query(Sponsor).filter_by(game_id=id).first()
        
        if not game_state:
            return ResponseSchema(
                success=False,
                message="Same game doesn't exist"
            )

        publisher = None
        sponsor = None
        game=GameSchema.from_orm(game_state)
        developer=AccomplicesSchema.from_orm(developer_state)
        if publisher_state:
            publisher=AccomplicesSchema.from_orm(publisher_state)
        if sponsor_state:
            sponsor=AccomplicesSchema.from_orm(sponsor_state)

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


def get_all_game() -> ResponseSchema:
    with get_session() as session:
        game_state = session.query(Game).order_by(Game.inserted_at.desc()).all()
        
        data = GamesSchema.from_orm(game_state).dict(by_alias=True)["data"]
    
        logging.warning(data)

        return ResponseSchema(
            data=data,
            success=True
        )


def update_game(game: GameSchema, developer: CompanySchema, publisher: CompanySchema, sponsor: CompanySchema, genre: GenreSchema, image) -> ResponseSchema:

    with get_session() as session:
        game_state = session.query(Game).filter_by(id=game.id).first()
        developer_state = session.query(Developer).filter_by(game_id=game.id).first()
        publisher_state = session.query(Publisher).filter_by(game_id=game.id).first()
        sponsor_state = session.query(Sponsor).filter_by(game_id=game.id).first()
        genre_state = session.query(Genre).filter_by(id=game.genre_id).first()

        game_state.title = game.title
        game_state.description = game.description
        game_state.date = game.date

        logging.warning(game.description)
        logging.warning(game_state.description)

        if genre.id != genre_state.id:
            game.genre_id = genre.id

        new_image = upload(image).data
        if new_image:
            game_state.image_id = new_image.id

        session.commit()

        logging.warning(developer_state)
        logging.warning(publisher_state)
        logging.warning(sponsor_state)
        logging.warning(developer)
        logging.warning(publisher)
        logging.warning(sponsor)

        if not developer and developer_state:
            session.delete(developer_state)
            logging.warning(developer_state)
            session.commit()
        
        if developer:
            if developer_state:
                session.delete(developer_state)
                session.commit()
            developer_state = Developer().fill(
                company_id=developer.id, 
                game_id=game.id,
                )
            session.add(developer_state)
            logging.warning(developer_state)
            session.commit()
        
        if not publisher and publisher_state:
            session.delete(publisher_state)
            logging.warning(publisher_state)
            session.commit()
        
        if publisher:
            if publisher_state:
                session.delete(publisher_state)
                session.commit()
            publisher_state = Publisher().fill(
                company_id=publisher.id, 
                game_id=game.id,
                )
            session.add(publisher_state)
            logging.warning(publisher_state)
            session.commit()
        
        if not sponsor and sponsor_state:
            session.delete(sponsor_state)
            logging.warning(sponsor_state)
            session.commit()

        if sponsor:
            if sponsor_state:
                session.delete(sponsor_state)
                session.commit()
            sponsor_state = Sponsor().fill(
                company_id=sponsor.id, 
                game_id=game.id,
                )
            session.add(sponsor_state)
            logging.warning(sponsor_state)
            session.commit()
    
    session.commit()
            

    return ResponseSchema(
        message="Game updated",
        success=True
    )


def delete_game(id: str) -> ResponseSchema:

    with get_session() as session:
        game_state = session.query(Game).filter_by(id=id).first()

        if not game_state:
            return ResponseSchema(
                success=False,
                message="Same genre doesn't exist"
            )

        session.delete(game_state)
        session.commit()

        return ResponseSchema(
            data=GameSchema.from_orm(game_state),
            message="Genre deleted",
            success=True
        )

