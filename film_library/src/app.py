from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import DevConfig, TestingConfig


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(is_tests: bool = False):
    app = Flask(__name__)
    if is_tests:
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevConfig)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db, directory='migrations')

    from src.views.films import film_blueprint
    from src.views.auth import auth_blueprint

    app.register_blueprint(film_blueprint)
    app.register_blueprint(auth_blueprint)

    return app
