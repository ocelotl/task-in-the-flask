from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from .models import Task, User
from .database import database
from logging import getLogger, ERROR
from app.user_authentication import verify_password, hash_password


_logger = getLogger(__name__)
_logger.setLevel(ERROR)

blueprint = Blueprint("routes", __name__)


@blueprint.route("/hello", methods=["GET"])
def hello():
    return "hello"


@blueprint.route("/get_tasks", methods=["GET"])
def get_tasks():

    result = []

    for task in Task.query.all():
        result.append(
            {
                "id": task.id,
                "title": task.title,
                "status": task.status
            }
        )

    return jsonify(result)


@blueprint.route("/create_task", methods=["POST"])
def create_tasks():

    data = request.json

    task = Task(title=data["title"], status=data["status"])

    # Calling add and later commit is done for efficiency reasons and to ensure
    # atomicity of the transaction.
    database.session.add(task)

    try:
        database.session.commit()
        return jsonify(message="Task created successfully"), 201

    except Exception:
        database.session.rollback()
        _logger.exception("Unable to commit to database")
        return jsonify(message="There was an error"), 500


@blueprint.route("/login", methods=["POST"])
def login():

    username = request.json["username"]
    password = request.json["password"]

    user = User.query.filter_by(username=username).first()

    if not user or not verify_password(password, hash_password(user.password)):
        return jsonify({"msg": "Invalid username or password"})

    return jsonify(
        access_token=create_access_token(user.username)
    )


@blueprint.route("/protected", methods=["GET"])
@jwt_required()
def protected():

    return jsonify(logged_in_as=get_jwt_identity()), 200
