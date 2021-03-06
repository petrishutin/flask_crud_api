from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_apispec import MethodResource, marshal_with, use_kwargs
from flask_apispec.annotations import doc

from app.db.db_utils import get_todo, get_todos, create_new_todo, update_todo, delete_todo
from app.utils.utils import check_username_match_resource_name
from app.schemas import ToDoSchemaIn, ToDoReadSchemaOut, ToDoCreateUpdateDeleteSchemaOut


class ToDosGetByIdPutDelete(Resource, MethodResource):
    @doc(tags=['TODOs'], description='Get ToDos by id')
    @jwt_required()
    @check_username_match_resource_name
    @marshal_with(ToDoReadSchemaOut)
    def get(self, username, todo_id=0, **kwargs):
        """Get ToDos by id"""
        return get_todo(username, todo_id)

    @doc(tags=['TODOs'], description='Update Todos by id')
    @jwt_required()
    @check_username_match_resource_name
    @use_kwargs(ToDoSchemaIn, location='json')
    @marshal_with(ToDoCreateUpdateDeleteSchemaOut)
    def put(self, username, todo_id, **kwargs):
        """Update Todos by id"""
        text = request.json.get('text', None)
        status = request.json.get('status', None)
        update_todo(username=username, todo_id=todo_id, text=text,
                    status=status)
        return {'todo_id': todo_id, 'result': 'updated'}, 202

    @doc(tags=['TODOs'], description='Delete Todos by id')
    @jwt_required()
    @check_username_match_resource_name
    @marshal_with(ToDoCreateUpdateDeleteSchemaOut)
    def delete(self, username, todo_id):
        """Delete ToDos by id"""
        delete_todo(username, todo_id)
        return {'todo_id': todo_id, 'result': 'deleted'}, 200


class ToDosGetAllPost(Resource, MethodResource):
    @doc(tags=['TODOs'], description='Get list of ToDos')
    @jwt_required()
    @check_username_match_resource_name
    @marshal_with(ToDoReadSchemaOut(many=True))
    def get(self, username):
        """Get list of ToDos"""
        return get_todos(username)

    @doc(tags=['TODOs'], description='Create new ToDos record')
    @jwt_required()
    @check_username_match_resource_name
    @use_kwargs(ToDoSchemaIn, location='json')
    @marshal_with(ToDoCreateUpdateDeleteSchemaOut)
    def post(self, username, **kwargs):
        """Create new ToDos record"""
        text = request.json.get('text', None)
        status = request.json.get('status', None)
        todo_id = create_new_todo(username, text, status)
        return {'todo_id': todo_id, 'result': 'created'}, 201
