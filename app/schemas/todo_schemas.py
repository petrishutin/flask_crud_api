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


class ToDoSchemaOut(Schema):
    id = fields.Integer()
    text = fields.Str()
    status = fields.Str()
    create_time = fields.Str()
    update_time = fields.Str()
