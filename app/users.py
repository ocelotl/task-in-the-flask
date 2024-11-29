from flask import Blueprint, jsonify

bp_users = Blueprint('users', __name__)


@bp_users.route('/register', methods=['POST'])
def register_user():
    # User registration logic here
    return jsonify(message="User registered successfully"), 201


@bp_users.route('/login', methods=['POST'])
def login_user():
    # User login logic here
    return jsonify(message="User logged in successfully"), 200
