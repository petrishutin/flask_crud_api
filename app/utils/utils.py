from functools import wraps

from flask_jwt_extended import current_user
from werkzeug.exceptions import UnprocessableEntity, Unauthorized


def check_passwords_mismatching(password1: str, password2: str):
    if password1 != password2:
        raise UnprocessableEntity('Passwords does not match')


def check_username_match_resource_name(func):
    """decorator to check if current user can access resource"""
    @wraps(func)
    def checker(*args, **kwargs):
        if current_user.username != kwargs['username']:
            raise Unauthorized(
                f"User {current_user.username} not authorized to get resource /todos/{kwargs['username']}"
            )
        return func(*args, **kwargs)

    return checker
