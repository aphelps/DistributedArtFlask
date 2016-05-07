from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.autodoc import Autodoc

from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
auto = Autodoc()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    auto.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .modes import modes as modes_blueprint
    app.register_blueprint(modes_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
