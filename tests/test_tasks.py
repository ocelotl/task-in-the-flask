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

    yield client

    with app.app_context():
        database.session.query(Task).delete()
        database.session.commit()
        database.session.remove()
        database.drop_all()


def test_get_tasks(setup_teardown):

    with setup_teardown.application.app_context():
        task = Task(title="New task", status="Ready")
        database.session.add(task)
        database.session.commit()

    response = setup_teardown.get("/get_tasks").get_json()

    assert response[0]["id"] == 1
    assert response[0]["status"] == "Ready"
    assert response[0]["title"] == "New task"


def test_create_task(setup_teardown):

    response = setup_teardown.post(
        "/create_task",
        json={
            "title": "Another task",
            "status": "Pending",
        }
    )

    assert response.status_code == 201

    with setup_teardown.application.app_context():
        tasks = database.session.query(Task).all()

    assert len(tasks) == 1

    assert tasks[0].id == 1
    assert tasks[0].status == "Pending"
    assert tasks[0].title == "Another task"
