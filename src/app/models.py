"""
This model holds the classes that represent the objects that go in the
database.
"""

from .database import database
from sqlalchemy.dialects.sqlite import JSON


class Task(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(120))
    status = database.Column(
        database.Enum(
            "pending", "in_progress", "ready", "blocked", name="status"
        ),
        nullable=False
    )
    tags = database.Column(JSON, default=[])


class User(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(
        database.String(120), unique=True, nullable=False
    )
    password = database.Column(
        database.String(120), unique=True, nullable=False
    )
