"""
This module holds the function that creates the app object.
"""

from flask import Flask
from flask_graphql import GraphQLView
from flask_jwt_extended import JWTManager
from .routes import blueprint
from .database import database
from .schema import schema


def create_app(configuration_filename=None):
    app = Flask(__name__)

    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
    )

    # The secret key is to be replaced with an actual secret key, not something
    # that is commited to the repo.
    app.config["JWT_SECRET_KEY"] = "secret-key"

    if configuration_filename is not None:
        # This loads the config objects from configuration_filename into the
        # app.config attribute.
        app.config.from_pyfile(configuration_filename)

    else:
        # Configure the database URI (e.g., SQLite in this case)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the app
    database.init_app(app)

    app.register_blueprint(blueprint)

    JWTManager(app)

    with app.app_context():
        database.create_all()
    return app
