from flask import Flask, Response, json
from flask_cors import CORS

import src.models
from src.utils.json_encoder import CustomJSONEncoder
from src.api.account import account
from src.api.genre import genre
from src.api.company import company
from src.api.image import image
from src.api.game import game
from settings import app_config


cors = CORS()


def create_app():
    app = Flask(__name__)
    app_settings = app_config.Settings()
    app.config["SQLALCHEMY_DATABASE_URI"] = app_settings.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = app_settings.SQLALCHEMY_TRACK_MODIFICATIONS
    app.json_encoder = CustomJSONEncoder
    cors.init_app(app)

    app.register_blueprint(account, url_prefix='/api/account')
    app.register_blueprint(genre, url_prefix='/api/genre')
    app.register_blueprint(company, url_prefix='/api/company')
    app.register_blueprint(image, url_prefix='/api/image')
    app.register_blueprint(game, url_prefix='/api/game')

    # @app.errorhandler(NotFound)
    # def handle_not_found_exception(error):
    #     app.logger.exception(error)
    #     return Response(
    #         "https://plitkazavr.ru/images/Original-Style/Victorian-Floor-Tiles/Revival-Grey-Rectangle-7.5x30.5.jpg",
    #         status=200, content_type="application/json")

    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.exception(error)
        return Response(json.dumps({
            "success": False,
            "message": str(error),
        }), status=400, content_type="application/json")


    @app.route('/')
    def home():
        return Response(
            json.dumps(
                {
                    "message":"hello"
                }
            ),
            status=200,
            content_type="application/json"
        )

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
