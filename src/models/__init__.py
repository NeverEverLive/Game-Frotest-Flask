from src.models.base_model import get_session, set_session, BaseModel

from src.models.user import User
from src.models.blacklist import BlackList
from src.models.article import Article
from src.models.company import Company
from src.models.developer import Developer
from src.models.publisher import Publisher
from src.models.sponsor import Sponsor
from src.models.game import Game
from src.models.genre import Genre
from src.models.image import Image
from src.models.logger import Logger

set_session()


from src.schema.user import UserSchema
from src.models.user import RoleEnum
from src.models.base_model import get_session
from sqlalchemy.dialects.postgresql import insert

with get_session() as session:
    """DDL при создании таблицы добавляет пользователя admin"""
    admin_user = {
        # "id": uuid.uuid4(),
        "username": "admin",
        "password": "123"
    }

    serializing_data = UserSchema.parse_obj(admin_user)
    ddl = insert(
            User
        ).values(
            id=serializing_data.id,
            username=serializing_data.username,
            hash_password=serializing_data.hash_password,
            role=RoleEnum.editor,
        ).on_conflict_do_nothing(
            index_elements=['username']
        )
    
    session.execute(ddl)
    session.commit()