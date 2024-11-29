from app import create_app, database
from pathlib import Path


def test_get_tasks():

    app = create_app(Path(__file__).parent.joinpath("config.py"))
    client = app.test_client()

    # This context provides the necessary context for Flask to access and
    # manage application-specific data like configurations and such. Normally
    # the application context is created automatically during a request
    # lifecycle, but in testing there is no active request, so the application
    # context can be accessed with app_context.
    with app.app_context():
        database.create_all()

    assert client.get("/tasks").get_json()["a"] == "b"
