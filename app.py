from flask import Flask, Response, json
from settings import app_config
import src.models
from flask_cors import CORS

cors = CORS()


def create_app():
    app = Flask(__name__)
    app_settings = app_config.Settings()
    app.config["SQLALCHEMY_DATABASE_URI"] = app_settings.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = app_settings.SQLALCHEMY_TRACK_MODIFICATIONS
    cors.init_app(app)
    from api.account import account
    app.register_blueprint(account, url_prefix='/account')

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
