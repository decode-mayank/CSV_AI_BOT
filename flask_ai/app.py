import os

from dotenv import load_dotenv
from flask import Flask, redirect, url_for
from flask_cors import CORS
from flask_migrate import Migrate, upgrade
from flask_smorest import Api

from resources.routes import pblp as ProductBlueprint
from resources.routes import blp as ChatBotBlueprint
from db import db

load_dotenv()

app = Flask(__name__)


MIGRATIONS_FOLDER = "./migrations" if "flask_ai" in os.getcwd() else "flask_ai/migrations"
print(MIGRATIONS_FOLDER)

@app.route('/')
def home():
    return redirect(url_for('api-docs.openapi_swagger_ui'))


def create_app():
    CORS(app)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Chatbot API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}@{os.getenv("DATABASE_HOST")}:{os.getenv("DATABASE_PORT")}/{os.getenv("DATABASE_NAME")}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db, directory=MIGRATIONS_FOLDER)

    api = Api(app)

    api.register_blueprint(ProductBlueprint)
    api.register_blueprint(ChatBotBlueprint)

    return app


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        # Uncomment below line to run migrations
        # upgrade()
        port = int(os.getenv('FLASK_PORT', 5000))
        app.run(host='0.0.0.0', port=port)
