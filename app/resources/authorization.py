from flask import request, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from flask_restful import Resource
from flask_apispec import MethodResource, use_kwargs
from flask_apispec.annotations import doc

from app.db.db_utils import get_user_instance
from app.schemas import UserLogInSchema


class LogIn(Resource, MethodResource):
    @doc(tags=['LogIn'], description='method to login')
    @use_kwargs(UserLogInSchema, location='json')
    def post(self, **kwargs):
        """get JWT token with payload"""
        username: str = request.json.get("username", None)
        password: str = request.json.get("password", None)
        user = get_user_instance(username, password)
        return {"access_token": create_access_token(identity=user)}, 200


class LogOut(Resource, MethodResource):
    @doc(tags=['LogOut'], description='method to logout')
    @jwt_required()
    def get(self):
        """LogOut"""
        jti = get_jwt()["jti"]
        current_app.config['JWT_BLOCK_LIST'].add(jti)
        return {"result": "Token revoked"}, 200
