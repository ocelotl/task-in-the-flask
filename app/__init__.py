from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from celery import Celery

db = SQLAlchemy()


def create_app():
    # This is a special function that follows the pattern called Application
    # Factory.
    # This function makes it possible to separate the app creation from its
    # configuration, and avoids having configuration settings in the global
    # app instance.
    # This function makes it possible to initialize extensions like SQLAlchemy
    # or Celery after the app is created.
    app = Flask(__name__)

    # When writing tests, you can create a new app with a different
    # configuration.
    app.config.from_object('instance.config.Config')

    # Initialize extensions
    db.init_app(app)

    # Register routes
    from . import routes
    # Blueprints are a way to organize the Flask app into smaller and reusable
    # modules. Blueprints allow you to break the app into distinct components,
    # each with its own set of routes, templates, static files and such.
    app.register_blueprint(routes.bp)

    return app


def create_celery_app(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery
