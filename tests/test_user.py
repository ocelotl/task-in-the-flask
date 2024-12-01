from app.user_authentication import hash_password, verify_password
from app.models import User
from app import database, create_app
from pytest import fixture
from pathlib import Path


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
        database.session.query(User).delete()
        database.session.commit()
        database.session.remove()
        database.drop_all()


def test_password():
    assert verify_password("asldmfo23#v*m", hash_password("asldmfo23#v*m"))


def test_login(setup_teardown):

    with setup_teardown.application.app_context():
        user = User(username="user_0", password="password_0")
        database.session.add(user)
        database.session.commit()

    response = setup_teardown.post(
        "/login",
        json={
            "username": "user_0",
            "password": "password_0",
        }
    )

    assert response.status_code == 200

    response = setup_teardown.get(
        "/protected",
        headers={
            "Authorization": f"Bearer {response.json['access_token']}"
        }
    )

    assert response.json["logged_in_as"] == "user_0"
