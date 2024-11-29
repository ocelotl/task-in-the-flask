from flask import Blueprint, jsonify

blueprint = Blueprint("routes", __name__)


@blueprint.route("/tasks", methods=["GET"])
def get_tasks():

    return jsonify({"a": "b"})
