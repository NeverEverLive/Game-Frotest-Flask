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