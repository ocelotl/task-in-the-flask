from flask import Blueprint, jsonify
from .models import Task

bp = Blueprint('routes', __name__)


@bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])
