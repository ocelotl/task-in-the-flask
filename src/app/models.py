from .database import database


class Task(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(120))
    status = database.Column(database.String(20), default="Pending")
