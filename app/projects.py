from flask import Blueprint, request, jsonify
from .models import Project, db

bp_projects = Blueprint('projects', __name__)


@bp_projects.route('/', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([project.to_dict() for project in projects])


@bp_projects.route('/', methods=['POST'])
def create_project():
    data = request.json
    project = Project(name=data['name'], description=data['description'])
    db.session.add(project)
    db.session.commit()
    return jsonify(message="Project created successfully"), 201
