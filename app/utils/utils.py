from functools import wraps
from typing import List

from flask import request
from flask_jwt_extended import current_user
from werkzeug.exceptions import BadRequest, Unauthorized, ImATeapot


def check_passwords_mismatching(password1: str, password2: str):
    if password1 != password2:
        raise BadRequest('Passwords does not match')


def check_password_length(password: str):
    if len(password) < 6:
        raise BadRequest('password to short. Min length is 6 chars')


def check_empty_fields(fields: List[str], req):
    empty_fields = []
    for field in fields:
        if not bool(req[field].strip()):
            empty_fields.append(field)
    if empty_fields:
        raise BadRequest(f'Empty fields: {empty_fields}')


def check_missing_fields(fields: List[str], req):
    """Check if fields present in request"""
    if not req:
        BadRequest(f'No payload')
    missing_fields = []
    for field in fields:
        if field not in req:
            missing_fields.append(field)
    if missing_fields:
        raise BadRequest(f'Missing fields: {missing_fields}')


def check_is_ascii(field: str):
    if not field.isascii():
        raise BadRequest('String should contain ASCII chars only')


def check_fields(needed_fields):
    """decorator to validate incoming fields"""
    def fields_checker(func):
        @wraps(func)
        def check(*args, **kwargs):
            check_missing_fields(needed_fields, request.json)
            check_empty_fields(needed_fields, request.json)
            return func(*args, **kwargs)
        return check
    return fields_checker


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
