from flask import request
from flask_restful import Resource
from flask_apispec import MethodResource
from werkzeug.exceptions import Conflict

from app.db.db_utils import user_does_exists, create_user, get_user_instance, \
    update_user_password
from app.utils.utils import check_fields, check_is_ascii, \
    check_passwords_mismatching, check_password_length


class Users(Resource, MethodResource):
    def post(self):
        """create new user"""
        username: str = request.json.get("username", None)
        password1: str = request.json.get("password1", None)
        password2: str = request.json.get("password2", None)
        check_is_ascii(username)
        check_passwords_mismatching(password1, password2)
        check_password_length(password1)
        if user_does_exists(username):
            raise Conflict('User Already exist')
        create_user(username, password1)
        return {'result': f'New user {username} successfully created'}, 201

    def put(self):
        """update user password"""
        username: str = request.json.get("username", None)
        old_password: str = request.json.get("old_password", None)
        password1: str = request.json.get("password1", None)
        password2: str = request.json.get("password2", None)
        user = get_user_instance(username, old_password)
        check_passwords_mismatching(password1, password2)
        check_password_length(password1)
        update_user_password(user, password1)
        return {'result': 'Password successfully updated!'}, 202
