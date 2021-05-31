from flask import request, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from app.db.db_utils import get_user_instance
from app.utils.utils import check_fields


class LogIn(Resource):
    @check_fields(['username', 'password'])
    def post(self):
        """get JWT token with payload"""
        username: str = request.json.get("username", None)
        password: str = request.json.get("password", None)
        user = get_user_instance(username, password)
        return {"access_token": create_access_token(identity=user)}, 200


class LogOut(Resource):
    @jwt_required()
    def get(self):
        """LogOut"""
        jti = get_jwt()["jti"]
        if not jti:
            raise BadRequest('Bearer token required')
        current_app.config['JWT_BLOCK_LIST'].add(jti)
        return {"result": "Token revoked"}, 200


