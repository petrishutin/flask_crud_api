from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_apispec import MethodResource
from werkzeug.exceptions import BadRequest

from app.db.db_utils import (
    get_todo, get_todos, create_new_todo, update_todo, delete_todo
)
from app.utils.utils import check_username_match_resource_name, check_fields


class ToDosGetByIdPutDelete(Resource, MethodResource):
    @jwt_required()
    @check_username_match_resource_name
    def get(self, username, todo_id=0):
        """Get ToDos by id"""
        return get_todo(username, todo_id)

    @jwt_required()
    @check_username_match_resource_name
    def put(self, username, todo_id):
        """Update Todos by id"""
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
        """Delete ToDos by id"""
        delete_todo(username, todo_id)
        return {'result': f'Todo id:{todo_id} successfully deleted!'}, 200


class ToDosGetAllPost(Resource, MethodResource):
    @jwt_required()
    @check_username_match_resource_name
    def get(self, username):
        """Get list of ToDos"""
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
        todo_id = create_new_todo(username, text, status)
        return {'result': todo_id}, 201
