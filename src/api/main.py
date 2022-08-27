from base64 import b64encode
from flask import render_template, Blueprint, request
from src.models.developer import Developer
from src.models.publisher import Publisher
from src.models.sponsor import Sponsor

from src.api.utils import authorization
from src.operators.image import get_image
from src.operators.company import get_all_companies, get_company
from src.operators.genre import get_genre
from src.operators.user import get_user
from src.operators.game import get_all_game, get_game
from src.operators.article import get_all_article, get_article
from src.schema.game import GameSchema


main = Blueprint("main", __name__)


@main.route('/')
# @authorization
def home():
    
    return render_template(
        "index.html",
        # token = token,
        request=request,
        queryset=get_all_article().data
    )

@main.route('/detail/<string:id>')
# @authorization
def detail(id):

    article = get_article(id).data

    game_id = article.game_id
    
    user_id = article.user_id
    user = get_user(user_id)["user"]
    
    game_info = get_game(game_id)
    game = game_info.data.game

    image, _ = get_image(game.image_id)
    image = b64encode(image).decode("utf-8")
    genre = get_genre(game.genre_id).data
    
    developer = game_info.data.developer
    developer_company = get_company(developer.company_id).data
    sponsor_company = None
    if game_info.data.sponsor:
        sponsor = game_info.data.sponsor
        sponsor_company = get_company(sponsor.company_id).data
    
    publisher_company = None
    if game_info.data.publisher:
        publisher = game_info.data.publisher
        publisher_company = get_company(publisher.company_id).data
    

    return render_template(
        "detail.html",
        # token=token,
        article=article,
        game=game,
        developer=developer_company,
        sponsor=sponsor_company,
        publisher=publisher_company,
        user=user,
        genre=genre,
        image=image
    )


@main.route("/edit")
def edit_page():
    return render_template("edit.html")


@main.route("/edit_game")
def edit_game_page():
    data = []
    games = get_all_game().data

    for game in games:
        genre = get_genre(game["genre_id"]).data
        image, _ = get_image(game["image_id"])
        image = b64encode(image).decode("utf-8")

        developer = Developer.get_by_game_id(game["id"])
        publisher = Publisher.get_by_game_id(game["id"])
        sponsor = Sponsor.get_by_game_id(game["id"])

        publisher_company = None
        sponsor_company = None
        developer_company = get_company(developer.company_id).data
        if publisher:
            publisher_company = get_company(publisher.company_id).data
        if sponsor:
            sponsor_company = get_company(sponsor.company_id).data

        data.append({
            "game": GameSchema.parse_obj(game),
            "image": image,
            "genre": genre,
            "developer": developer_company,
            "publisher": publisher_company,
            "sponsor": sponsor_company
        })

    return render_template(
        "edit_game.html",
        enum_data=enumerate(data),
    )


@main.route("/edit_company")
def edit__companies_page():
    companies = get_all_companies().data
        
    return render_template(
        "edit_company.html",
        companies=companies
    )


