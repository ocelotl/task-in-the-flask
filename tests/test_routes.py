from app import database, create_app
from pathlib import Path
from app.models import Task
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

    yield client

    with app.app_context():
        database.session.query(Task).delete()
        database.session.commit()
        database.session.remove()
        database.drop_all()


def test_create_task(setup_teardown):

    response = setup_teardown.post(
        "/create_task",
        json={
            "title": "Another task",
            "status": "pending",
        }
    )

    assert response.status_code == 201

    with setup_teardown.application.app_context():
        tasks = database.session.query(Task).all()

    assert len(tasks) == 1

    assert tasks[0].id == 1
    assert tasks[0].status == "pending"
    assert tasks[0].title == "Another task"
