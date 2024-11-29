from flask import Blueprint, jsonify, request
from .models import Task
from .database import database
from logging import getLogger, ERROR


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
