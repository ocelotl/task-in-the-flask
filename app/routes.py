from flask import Blueprint, jsonify
from .models import Task

# A Blueprint object works similarly to a Flask application object but it is
# not actually an application, but a _blueprint_ of how to construct or
# extend an application.
# A Flask Blueprint is a set of operations which can be registered on an
# application, even multiple times.
# Blueprints can share application configuration and can change an application
# object with being registered, but they cannot be unregistered without
# destroying the application object.
# Blueprints record operations that are executed when registered on an
# application.
bp = Blueprint('routes', __name__)


@bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])
