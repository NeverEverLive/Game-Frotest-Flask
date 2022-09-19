from base64 import b64encode
import datetime
import logging
from flask import render_template, Blueprint, request
from src.operators.logger import apply
from src.schema.article import ArticleSchema
from src.schema.company import CompanySchema
from src.operators.accompile import create_accompile
from src.models.developer import Developer
from src.models.publisher import Publisher
from src.models.sponsor import Sponsor

from src.api.utils import authorization
from src.operators.image import get_image, upload
from src.operators.company import create_company, delete_company, get_all_companies, get_company, get_company_by_name, update_company
from src.operators.genre import get_all_genries, get_genre, get_genre_by_title
from src.operators.user import create_user, get_user, login_user
from src.operators.game import create_game, delete_game, get_all_game, get_game, update_game
from src.operators.article import create_article, get_all_article, get_article
from src.schema.game import GameCompanyRelationSchema, GameSchema


main = Blueprint("main", __name__)


current_user = None


@main.route('/')
# @authorization
def home(authorization_message=None):
    try:
        data = get_all_article().data
    except:
        data = []

    try:
        games = get_all_game().data
    except:
        games = []
        
    logging.warning(current_user)

    return render_template(
        "index.html",
        # token = token,
        request=request,
        current_user=current_user,
        authorization_message=authorization_message,
        queryset=data,
        games=games
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
        current_user=current_user,
        user=user,
        genre=genre,
        image=image
    )


@main.route("/edit")
def edit_page():
    return render_template(
        "edit.html",
        current_user=current_user,
    )


@main.route("/edit_game")
def edit_game_page(success=False, success_update=False, success_delete=False, seccess_backroll=False):
    
    data = []
    companies = get_all_companies().data
    genries = get_all_genries().data

    try:
        games = get_all_game().data
    except:
        games = []

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
        success=success,
        success_update=success_update,
        success_delete=success_delete,
        seccess_backroll=seccess_backroll,
        current_user=current_user,
        companies=companies,
        genries=genries
    )


@main.route("/update_game/<string:id>")
def update_game_endpoint(id):

    game_info = get_game(id).data

    game = game_info.game
    current_developer = game_info.developer
    current_developer = get_company(current_developer.company_id).data
    
    current_publisher = game_info.publisher
    if current_publisher:
        current_publisher = get_company(current_publisher.company_id).data

    current_sponsor = game_info.sponsor
    if current_sponsor:
        current_sponsor = get_company(current_sponsor.company_id).data

    current_genre = get_genre(game.genre_id).data
    image, _ = get_image(game.image_id)
    current_image = image = b64encode(image).decode("utf-8")
    
    companies = get_all_companies().data
    genries = get_all_genries().data

    return render_template(
        "update_game.html",
        game=game,
        current_developer=current_developer,
        current_publisher=current_publisher,
        current_sponsor=current_sponsor,
        current_genre=current_genre,
        current_image=current_image,
        current_user=current_user,
        companies=companies,
        genries=genries
    )


@main.post("/submit_game")
def submit_update():

    request_form = request.form
    request_file = request.files

    logging.warning(request_form)

    game_id = request_form["GameId"]
    game = get_game(game_id).data.game

    game_title = request_form["inputTitle"]
    game_description = request_form["inputDescription"]
    game_date = request_form["inputDate"]
    
    game.title = game_title
    game.description = game_description
    game.date = game_date

    genre = request_form["selectGenre"] if request_form["selectGenre"] != "Select genre" else ""
    genre = get_genre_by_title(genre).data
    
    developer = request_form["selectDeveloper"] if request_form["selectDeveloper"] != "Select developer" else ""
    developer_company = None
    if developer:
        developer_company = get_company_by_name(developer).data

    publisher = request_form["selectPublisher"] if request_form["selectPublisher"] != "Select publisher" else ""
    publisher_company = None
    if publisher:
        publisher_company = get_company_by_name(publisher).data
    
    sponsor = request_form["selectSponsor"] if request_form["selectSponsor"] != "Select sponsor" else ""
    sponsor_company = None
    if sponsor:
        sponsor_company = get_company_by_name(sponsor).data

    image = request_file["fileImage"]

    update_game(game, developer_company, publisher_company, sponsor_company, genre, image)


    return edit_game_page(
        success_update=True,
        )

@main.get("/delete_game/<string:id>")
def delete_game_edpoint(id):
    delete_game(id)

    return edit_game_page(
        success_delete=True
        )
    

@main.post("/create_game")
def create_game_edpoint():
    request_form = request.form
    request_file = request.files

    game_title = request_form["inputTitle"]
    game_description = request_form["inputDescription"]
    game_date = request_form["inputDate"]

    image = request_file["fileImage"]
    image = upload(image).data
    
    genre = request_form["selectGenre"] if request_form["selectGenre"] != "Select genre" else ""
    genre = get_genre_by_title(genre).data

    game = GameSchema(
        title=game_title,
        description=game_description,
        date=game_date,
        image_id=image.id,
        genre_id=genre.id
    )

    developer = request_form["selectDeveloper"] if request_form["selectDeveloper"] != "Select developer" else ""
    developer_company = None
    if developer:
        developer_company = get_company_by_name(developer).data
        developer = create_accompile(developer_company, Developer, game.id).data

    publisher = request_form["selectPublisher"] if request_form["selectPublisher"] != "Select publisher" else ""
    publisher_company = None
    if publisher:
        logging.warning(1)
        publisher_company = get_company_by_name(publisher).data
        publisher = create_accompile(publisher_company, Publisher, game.id).data
    
    sponsor = request_form["selectSponsor"] if request_form["selectSponsor"] != "Select sponsor" else ""
    sponsor_company = None
    if sponsor:
        sponsor_company = get_company_by_name(sponsor).data
        sponsor = create_accompile(sponsor_company, Sponsor, game.id).data

    if not publisher:
        publisher = None
    if not sponsor:
        sponsor = None

    data = GameCompanyRelationSchema(
        game=game,
        developer=developer,
        publisher=publisher,
        sponsor=sponsor,
    )

    logging.warning(data)

    create_game(data)

    return edit_game_page(
        success=True
        )


@main.route("/edit_company")
def edit_companies_page(success=False, success_update=False, success_delete=False):
    companies = get_all_companies().data
        
    return render_template(
        "edit_company.html",
        companies=companies,
        current_user=current_user,
        success=success,
        success_update=success_update,
        success_delete=success_delete
    )


@main.post("/create_company")
def create_company_endpoint():
    request_form = request.form

    company_title = request_form["inputTitle"]
    company_description = request_form["inputDescription"]

    company = CompanySchema(
        name=company_title,
        description=company_description
    )

    create_company(company)

    return edit_companies_page(
        success=True,
        )


@main.route("/update_company/<string:id>")
def update_company_endpoint(id):

    company_info = get_company(id).data

    current_company_title = company_info.name
    current_company_description = company_info.description

    logging.warning("1")

    return render_template(
        "update_company.html",
        company=company_info,
        current_title=current_company_title,
        current_user=current_user,
        current_description=current_company_description
    )


@main.post("/submit_company")
def submit_update_company():

    request_form = request.form

    company = get_company(request_form["companyId"]).data

    company.name = request_form["inputTitle"]
    company.description = request_form["inputDescription"]

    update_company(company)

    return edit_companies_page(
        success_update=True

        )


@main.get("/delete_company/<string:id>")
def delete_company_edpoint(id):
    delete_company(id)

    return edit_companies_page(
        success_delete=True,
        )


@main.post("/create_article")
def create_article_endpoint():
    request_form = request.form

    article_title = request_form["inputTitle"]
    article_description = request_form["inputDescription"]
    article_date = request_form.get("inputDate", datetime.datetime.now())
    article_published = request_form.get("checkIsPusblished", False)
    game_id = request_form["selectGame"]
    logging.warning(game_id)
    article = ArticleSchema(
        title=article_title,
        description=article_description,
        date=article_date,
        is_published=article_published,
        game_id=game_id,
        user_id=current_user["id"]
    )
    
    create_article(article)

    return home()


# @main.route("/update_company/<string:id>")
# def update_company_endpoint(id):

#     company_info = get_company(id).data

#     current_company_title = company_info.name
#     current_company_description = company_info.description

#     logging.warning("1")

#     return render_template(
#         "update_company.html",
#         company=company_info,
#         current_title=current_company_title,
#         current_user=current_user,
#         current_description=current_company_description
#     )


# @main.post("/submit_company")
# def submit_update_company():

#     request_form = request.form

#     company = get_company(request_form["companyId"]).data

#     company.name = request_form["inputTitle"]
#     company.description = request_form["inputDescription"]

#     update_company(company)

#     return edit_companies_page(
#         success_update=True,
#         current_user=current_user,

#         )


# @main.get("/delete_company/<string:id>")
# def delete_company_edpoint(id):
#     delete_company(id)

#     return edit_companies_page(
#         success_delete=True,
#         current_user=current_user,
#         )



@main.get("/login")
def get_login_request_edpoint(error_message=None):
    
    logging.warning("1")

    return render_template(
        "login.html",
        current_user=current_user,
        error_message=error_message
        )


@main.post("/user/login")
def login_user_edpoint():
    
    request_form = request.form

    data = {
        "username": request_form["inputUsername"],
        "password": request_form["inputPassword"]
    }

    global current_user
    try:
        current_user = login_user(data)["user"]
    except ValueError as error:
        return get_login_request_edpoint(str(error))

    logging.warning(current_user)
        
    return home(authorization_message="You've successfully logged in")


@main.get("/register")
def get_signin_request_edpoint():
    
    logging.warning("1")

    return render_template(
        "register.html",
        current_user=current_user,
        )


@main.post("/user/register")
def register_user_edpoint():
    
    request_form = request.form

    data = {
        "username": request_form["inputUsername"],
        "password": request_form["inputPassword"]
    }

    global current_user
    
    current_user = create_user(data)["user"]["username"]

    logging.warning(current_user)
        
    return home(authorization_message="Your account seccessfuly created")


@main.get("/user/logout")
def logout_user_edpoint():
    global current_user

    current_user = None

    return home(authorization_message="You successfully logged out")


@main.post("/backroll")
def backroll():
    request_form = request.form

    logging.warning(request_form)

    limit = request_form["InputCount"]

    apply(limit)

    return edit_game_page(seccess_backroll=True)
