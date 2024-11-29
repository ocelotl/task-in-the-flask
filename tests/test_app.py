from app import create_app, database
from app.models import Task
from pathlib import Path
from pytest import fixture


@fixture
def setup_teardown():
    app = create_app(Path(__file__).parent.joinpath("config.py"))
    client = app.test_client()

    # This context provides the necessary context for Flask to access and
    # manage application-specific data like configurations and such. Normally
    # the application context is created automatically during a request
    # lifecycle, but in testing there is no active request, so the application
    # context can be accessed with app_context.
    with app.app_context():
        database.create_all()

    with app.app_context():
        task = Task(title="New task", status="Ready")
        database.session.add(task)
        database.session.commit()

    yield client

    with app.app_context():
        database.session.remove()
        database.drop_all()


def test_get_tasks(setup_teardown):

    result = setup_teardown.get("/get_tasks").get_json()

    assert result[0]["id"] == 1
    assert result[0]["status"] == "Ready"
    assert result[0]["title"] == "New task"
