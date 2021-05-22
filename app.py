from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token, JWTManager, jwt_required
from werkzeug.exceptions import BadRequest, NotFound

import config
from db_engine import initiate_db, Session
from models import User
from utils import (
    check_passwords_mismatching, check_password_length,
    check_username_match_resource_name, check_fields, check_is_ascii
)
from db_utils import (
    get_user_instance, create_user, user_does_exists, update_user_password,
    create_new_todo, get_todos, get_todo,
    update_todo, delete_todo
)

app = Flask(__name__, template_folder='.')
app.config.from_object(config)
api = Api(app)

jwt = JWTManager(app)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = Session.query(User).filter_by(username=identity).one_or_none()
    return user


class LogIn(Resource):
    @check_fields(['username', 'password'])
    def post(self):
        """get JWT token with payload"""
        username: str = request.json.get("username", None)
        password: str = request.json.get("password", None)
        user = get_user_instance(username, password)
        return {"access_token": create_access_token(identity=user)}, 200


class LogOut(Resource):
    def get(self, username=''):
        """LogOut"""
        if not username:
            return {'error': 'Username in path required'}, 400



class Users(Resource):
    @check_fields(['username', 'password1', 'password2'])
    def post(self):
        """create new user"""
        username: str = request.json.get("username", None)
        password1: str = request.json.get("password1", None)
        password2: str = request.json.get("password2", None)
        check_is_ascii(username)
        check_passwords_mismatching(password1, password2)
        check_password_length(password1)
        if user_does_exists(username):
            raise BadRequest('User Already exist')
        create_user(username, password1)
        return {'result': f'New user {username} successfully created'}, 201

    @check_fields(['username', 'password1', 'password2', 'old_password'])
    def put(self):
        """update user password"""
        username: str = request.json.get("username", None)
        old_password: str = request.json.get("old_password", None)
        password1: str = request.json.get("password1", None)
        password2: str = request.json.get("password2", None)
        user = get_user_instance(username, old_password)
        # check_passwords_mismatching(password1, password2)
        # check_password_length(password1)
        update_user_password(user, password1)
        return {'result': 'Password successfully updated!'}, 202


class ToDos(Resource):
    @jwt_required()
    @check_username_match_resource_name
    def get(self, username, todo_id=0):
        """Get list of ToDos"""
        if todo_id:
            return get_todo(username, todo_id)
        return get_todos(username)

    @jwt_required()
    @check_username_match_resource_name
    @check_fields(['text', 'status'])
    def post(self, username):
        """Create new ToDos record"""
        text = request.json.get('text', None)
        status = request.json.get('status', None)
        if status not in ['TODO', 'INPROGRESS', 'DONE', 'CANCELED']:
            raise BadRequest(
                "Status mast be 'TODO', 'INPROGRESS', 'DONE' or 'CANCELED'")
        create_new_todo(username, text, status)
        return {'result': 'New todo successfully created!'}, 201

    @jwt_required()
    @check_username_match_resource_name
    def put(self, username, todo_id):
        text = request.json.get('text', None)
        status = request.json.get('status', None)
        if status not in ['TODO', 'INPROGRESS', 'DONE', 'CANCELED']:
            raise BadRequest(
                "Status mast be 'TODO', 'INPROGRESS', 'DONE' or 'CANCELED'")
        update_todo(username=username, todo_id=todo_id, text=text,
                    status=status)
        return {'result': f'Todo id:{todo_id} successfully updated!'}, 202

    @jwt_required()
    @check_username_match_resource_name
    def delete(self, username, todo_id):
        delete_todo(username, todo_id)
        return {'result': f'Todo id:{todo_id} successfully deleted!'}, 200


api.add_resource(Users, '/users', '/users/')
api.add_resource(LogIn, '/login', '/login/')
api.add_resource(
    LogOut, '/logout', '/logout/', '/logout/<string:username>',
    '/logout/<string:username>/'
)
api.add_resource(
    ToDos, '/todos/<string:username>', '/todos/<string:username>/',
    '/todos/<string:username>/<int:todo_id>',
    '/todos/<string:username>/<int:todo_id>/'
)

if __name__ == '__main__':
    initiate_db()
    app.run(port=8080, debug=1)
