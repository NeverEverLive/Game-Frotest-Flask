

import logging
from uuid import uuid4
from src.operators.image import upload
from src.operators.article import delete_article
from src.models.genre import Genre
from src.models.article import Article
from src.models.logger import Logger
from src.schema.company import CompanySchema
from src.schema.genre import GenreSchema
from src.models.base_model import get_session
from src.models.game import Game
from src.models.developer import Developer
from src.models.publisher import Publisher
from src.models.sponsor import Sponsor
from src.schema.game import GameSchema, GamesSchema, GameCompanyRelationSchema
from src.schema.accomplices import AccomplicesSchema
from src.schema.response import ResponseSchema


def _create_developer(game, developer):
    developer.game_id = game.id
    developer_state = Developer().fill(**developer.dict())

    with get_session() as session:
        session.add(developer_state)
        session.commit()

        logger_data = {
            "id": uuid4(),
            "table": "developer",
            "action": "delete",
            "object_info": AccomplicesSchema.from_orm(developer).dict()
        }

        logger_state = Logger().fill(**logger_data)
        session.add(logger_state)
        session.commit()


def _create_publisher(game, publisher):
    publisher.game_id = game.id
    publisher_state = Publisher().fill(**publisher.dict())

    with get_session() as session:
        session.add(publisher_state)
        session.commit()

        logger_data = {
            "id": uuid4(),
            "table": "publisher",
            "action": "delete",
            "object_info": AccomplicesSchema.from_orm(publisher).dict()
        }

        logger_state = Logger().fill(**logger_data)
        session.add(logger_state)
        session.commit()


def _create_sponsor(game, sponsor):
    sponsor.game_id = game.id
    sponsor_state = Sponsor().fill(**sponsor.dict())

    with get_session() as session:
        session.add(sponsor_state)
        session.commit()

        logger_data = {
            "id": uuid4(),
            "table": "sponsor",
            "action": "delete",
            "object_info": AccomplicesSchema.from_orm(sponsor).dict()
        }

        logger_state = Logger().fill(**logger_data)
        session.add(logger_state)
        session.commit()


def _create_accomplices(data):
    if data.developer:
        _create_developer(data.game, data.developer)
    if data.publisher:
        _create_publisher(data.game, data.publisher)
    if data.sponsor:
        _create_sponsor(data.game, data.publisher)


def _delete_accompilices(developer_state, publisher_state, sponsor_state, session):
    if developer_state:
        for developer in developer_state:
            logger_data = {
                "id": uuid4(),
                "table": "developer",
                "action": "insert",
                "object_info": AccomplicesSchema.from_orm(developer).dict()
            }

            logger_state = Logger().fill(**logger_data)
            session.add(logger_state)
            session.commit()

            session.delete(developer)
            session.commit()

    if publisher_state:
        for publisher in publisher_state:
            logger_data = {
                "id": uuid4(),
                "table": "publisher",
                "action": "insert",
                "object_info": AccomplicesSchema.from_orm(publisher).dict()
            }

            logger_state = Logger().fill(**logger_data)
            session.add(logger_state)
            session.commit()

            session.delete(publisher)
            session.commit()

    if sponsor_state:
        for sponsor in sponsor_state:
            logger_data = {
                "id": uuid4(),
                "table": "sponsor",
                "action": "insert",
                "object_info": AccomplicesSchema.from_orm(sponsor).dict()
            }

            logger_state = Logger().fill(**logger_data)
            session.add(logger_state)
            session.commit()

            session.delete(sponsor)
            session.commit()


def create_game(data: GameCompanyRelationSchema) -> ResponseSchema:
    game_state = Game().fill(**data.game.dict())

    with get_session() as session:
        session.add(game_state)
        session.commit()

        logger_data = {
            "id": uuid4(),
            "table": "game",
            "action": "delete",
            "object_info": GameSchema.from_orm(game_state).dict()
        }

        logger_state = Logger().fill(**logger_data)
        session.add(logger_state)
        session.commit()

    _create_accomplices(data)

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

        return ResponseSchema(
            data=data,
            success=True
        )


def update_game(game: GameSchema, developer: CompanySchema, publisher: CompanySchema, sponsor: CompanySchema, genre: GenreSchema, image) -> ResponseSchema:

    with get_session() as session:
        game_state = session.query(Game).filter_by(id=game.id).first()

        logger_data = {
            "id": uuid4(),
            "table": "game",
            "action": "update",
            "object_info": GameSchema.from_orm(game_state).dict()
        }

        logger_state = Logger().fill(**logger_data)
        session.add(logger_state)
        session.commit()

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

        logging.warning(developer.id)
        logging.warning(developer_state.company_id)
        logging.warning(bool(developer))
        logging.warning(bool(developer_state))
        logging.warning(bool(str(developer.id) != str(developer_state.company_id)))

        if not developer and developer_state:
            session.delete(developer_state)
            logging.warning(developer_state)
            session.commit()

            logger_data = {
                "id": uuid4(),
                "table": "developer",
                "action": "insert",
                "object_info": AccomplicesSchema.from_orm(developer_state).dict()
            }

            logger_state = Logger().fill(**logger_data)
            session.add(logger_state)
            session.commit()
        
        elif developer and not developer_state:
            developer_state = Developer().fill(
                company_id=developer.id, 
                game_id=game.id,
                )
            session.add(developer_state)
            logging.warning(developer_state)
            session.commit()

            logger_data = {
                "id": uuid4(),
                "table": "developer",
                "action": "delete",
                "object_info": AccomplicesSchema.from_orm(developer_state).dict()
            }

            logger_state = Logger().fill(**logger_data)
            session.add(logger_state)
            session.commit()

        elif developer and developer_state and str(developer.id) != str(developer_state.company_id):
            session.delete(developer_state)
            session.commit()

            logger_data = {
                "id": uuid4(),
                "table": "developer",
                "action": "insert",
                "object_info": AccomplicesSchema.from_orm(developer_state).dict()
            }

            logger_state = Logger().fill(**logger_data)
            session.add(logger_state)
            session.commit()
            
            developer_state = Developer().fill(
                company_id=developer.id, 
                game_id=game.id,
                )
            session.add(developer_state)
            logging.warning(developer_state)
            session.commit()

            logger_data = {
                "id": uuid4(),
                "table": "developer",
                "action": "delete",
                "object_info": AccomplicesSchema.from_orm(developer_state).dict()
            }

            logger_state = Logger().fill(**logger_data)
            session.add(logger_state)
            session.commit()

        if not publisher and publisher_state:
            session.delete(publisher_state)
            logging.warning(publisher_state)
            session.commit()

            logger_data = {
                "id": uuid4(),
                "table": "publisher",
                "action": "insert",
                "object_info": AccomplicesSchema.from_orm(developer_state).dict()
            }

            logger_state = Logger().fill(**logger_data)
            session.add(logger_state)
            session.commit()
        
        elif publisher and not publisher_state:
            publisher_state = Publisher().fill(
                company_id=publisher.id, 
                game_id=game.id,
                )
            session.add(publisher_state)
            logging.warning(publisher_state)
            session.commit()

            logger_data = {
                "id": uuid4(),
                "table": "publisher",
                "action": "delete",
                "object_info": AccomplicesSchema.from_orm(publisher_state).dict()
            }

            logger_state = Logger().fill(**logger_data)
            session.add(logger_state)
            session.commit()

        elif publisher and publisher_state and str(publisher.id) != str(publisher_state.company_id):
            session.delete(publisher_state)
            session.commit()

            logger_data = {
                "id": uuid4(),
                "table": "publisher",
                "action": "insert",
                "object_info": AccomplicesSchema.from_orm(publisher_state).dict()
            }

            logger_state = Logger().fill(**logger_data)
            session.add(logger_state)
            session.commit()
            
            publisher_state = Publisher().fill(
                company_id=publisher.id, 
                game_id=game.id,
                )
            session.add(publisher_state)
            logging.warning(publisher_state)
            session.commit()

            logger_data = {
                "id": uuid4(),
                "table": "publisher",
                "action": "delete",
                "object_info": AccomplicesSchema.from_orm(publisher_state).dict()
            }

            logger_state = Logger().fill(**logger_data)
            session.add(logger_state)
            session.commit()

        if not sponsor and sponsor_state:
            session.delete(sponsor_state)
            logging.warning(sponsor_state)
            session.commit()

            logger_data = {
                "id": uuid4(),
                "table": "sponsor",
                "action": "insert",
                "object_info": AccomplicesSchema.from_orm(developer_state).dict()
            }

            logger_state = Logger().fill(**logger_data)
            session.add(logger_state)
            session.commit()

        elif sponsor and not sponsor_state:
            sponsor_state = Sponsor().fill(
                company_id=sponsor.id, 
                game_id=game.id,
                )
            session.add(sponsor_state)
            logging.warning(sponsor_state)
            session.commit()

            logger_data = {
                "id": uuid4(),
                "table": "sponsor",
                "action": "delete",
                "object_info": AccomplicesSchema.from_orm(sponsor_state).dict()
            }

            logger_state = Logger().fill(**logger_data)
            session.add(logger_state)
            session.commit()

        elif sponsor and sponsor_state and str(sponsor.id) != str(sponsor_state.company_id):
            session.delete(sponsor_state)
            session.commit()

            logger_data = {
                "id": uuid4(),
                "table": "sponsor",
                "action": "insert",
                "object_info": AccomplicesSchema.from_orm(sponsor_state).dict()
            }

            logger_state = Logger().fill(**logger_data)
            session.add(logger_state)
            session.commit()
            
            sponsor_state = Sponsor().fill(
                company_id=sponsor.id, 
                game_id=game.id,
                )
            session.add(sponsor_state)
            logging.warning(sponsor_state)
            session.commit()

            logger_data = {
                "id": uuid4(),
                "table": "sponsor",
                "action": "delete",
                "object_info": AccomplicesSchema.from_orm(sponsor_state).dict()
            }

            logger_state = Logger().fill(**logger_data)
            session.add(logger_state)
            session.commit()    

    session.commit()
            

    return ResponseSchema(
        message="Game updated",
        success=True
    )


def delete_game(id: str) -> ResponseSchema:

    with get_session() as session:
        article_state = session.query(Article).filter_by(game_id=id).all()
        logging.warning(article_state)

        developer_state = session.query(Developer).filter_by(game_id=id).all()
        logging.warning(developer_state)
        publisher_state = session.query(Publisher).filter_by(game_id=id).all()
        logging.warning(publisher_state)
        sponsor_state = session.query(Sponsor).filter_by(game_id=id).all()
        logging.warning(sponsor_state)
        
        for article in article_state:
            delete_article(article)
        
        _delete_accompilices(developer_state, publisher_state, sponsor_state, session)

        game_state = session.query(Game).filter_by(id=id).first()

        if not game_state:
            return ResponseSchema(
                success=False,
                message="Same game doesn't exist"
            )

        logger_data = {
            "id": uuid4(),
            "table": "game",
            "action": "insert",
            "object_info": GameSchema.from_orm(game_state).dict()
        }

        logger_state = Logger().fill(**logger_data)
        session.add(logger_state)
        session.commit()

        session.delete(game_state)
        session.commit()

        return ResponseSchema(
            data=GameSchema.from_orm(game_state),
            message="Genre deleted",
            success=True
        )

