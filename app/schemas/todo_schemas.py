from marshmallow import Schema, fields, validates
from werkzeug.exceptions import UnprocessableEntity
from flask import current_app


class ToDoSchemaIn(Schema):
    text = fields.Str()
    status = fields.Str(default='TODO')

    @validates('status')
    def validate_status(self, value):
        if value not in current_app.config['TODO_STATUSES']:
            raise UnprocessableEntity(f"Status mast be {current_app.config['TODO_STATUSES']}")


class ToDoReadSchemaOut(Schema):
    id = fields.Integer()
    text = fields.String()
    status = fields.String()
    create_time = fields.String()
    update_time = fields.String()


class ToDoCreateUpdateDeleteSchemaOut(Schema):
    todo_id = fields.Integer()
    result = fields.String()
