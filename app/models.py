# This file contains the SQLAlchemy database models.

from . import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    status = db.Column(db.String(20), default='To-Do')
