"""
This module holds the functions used for user authentication for the REST API.
"""


from bcrypt import hashpw, gensalt, checkpw


def hash_password(password):
    return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")


def verify_password(password, hashed):
    return checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
