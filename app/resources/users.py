from flask import request
from flask_restful import Resource
from flask_apispec import MethodResource
from werkzeug.exceptions import Conflict
from flask_apispec import use_kwargs
from flask_apispec.annotations import doc

from app.db.db_utils import user_does_exists, create_user, get_user_instance, update_user_password
from app.utils.utils import check_passwords_mismatching
from app.schemas import UserRegistrationSchemaIn, UserPasswordUpdateSchemaIn


class Users(Resource, MethodResource):
    @doc(tags=['Users'], description='Create new user with schema')
    @use_kwargs(UserRegistrationSchemaIn, location='json')
    def post(self, **kwargs):
        """create new user"""
        username: str = request.json.get("username", None)
        password1: str = request.json.get("password1", None)
        password2: str = request.json.get("password2", None)
        check_passwords_mismatching(password1, password2)
        if user_does_exists(username):
            raise Conflict('User Already exist')
        create_user(username, password1)
        return {'result': f'New user {username} successfully created'}, 201

    @doc(tags=['Users'], description='Update user`s password')
    @use_kwargs(UserPasswordUpdateSchemaIn, location='json')
    def put(self, **kwargs):
        """update user password"""
        username: str = request.json.get("username", None)
        old_password: str = request.json.get("old_password", None)
        password1: str = request.json.get("password1", None)
        password2: str = request.json.get("password2", None)
        check_passwords_mismatching(password1, password2)
        user = get_user_instance(username, old_password)
        update_user_password(user, password1)
        return {'result': 'Password successfully updated!'}, 202
