from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from app.db.db_utils import (
    get_todo, get_todos, create_new_todo, update_todo, delete_todo
)
from app.utils.utils import check_username_match_resource_name, check_fields


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
        todo_id = create_new_todo(username, text, status)
        return {'result': todo_id}, 201

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
