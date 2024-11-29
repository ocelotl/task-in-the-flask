from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .routes import blueprint


database = SQLAlchemy()


def create_app(configuration_filename):
    app = Flask(__name__)

    # This loads the config objects from configuration_filename into the
    # app.config attribute.
    app.config.from_pyfile(configuration_filename)

    database.init_app(app)
    app.register_blueprint(blueprint)

    return app
