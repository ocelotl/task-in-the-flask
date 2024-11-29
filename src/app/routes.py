from flask import Blueprint, jsonify
from .models import Task

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
