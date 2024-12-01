from flask import Flask
from flask_jwt_extended import JWTManager
from .routes import blueprint
from .database import database


def create_app(configuration_filename=None):
    app = Flask(__name__)

    # The secret key is to be replaced with an actual secret key, not something
    # that is commited to the repo.
    app.config["JWT_SECRET_KEY"] = "secret-key"

    if configuration_filename is not None:
        # This loads the config objects from configuration_filename into the
        # app.config attribute.
        app.config.from_pyfile(configuration_filename)
        database.init_app(app)

    app.register_blueprint(blueprint)

    JWTManager(app)

    return app
