from marshmallow import Schema, fields
from werkzeug.exceptions import UnprocessableEntity


def check_length(min_length: int, max_length: int, field_name: str):
    def length_checker(value):
        if len(value) < min_length:
            raise UnprocessableEntity(f'Min length of {field_name} field must be {min_length} or greater')
        if len(value) > max_length:
            raise UnprocessableEntity(f'Max length of {field_name} field must be {max_length} or smaller')
    return length_checker


class UserRegistrationSchemaIn(Schema):
    username = fields.Str(required=True, validate=check_length(6, 50, 'username'))
    password1 = fields.Str(required=True, validate=check_length(6, 32, 'password'))
    password2 = fields.Str(required=True)


class UserPasswordUpdateSchemaIn(Schema):
    username = fields.Str(required=True, validate=check_length(6, 50, 'username'))
    old_password = fields.Str(required=True)
    password1 = fields.Str(required=True, validate=check_length(6, 32, 'password'))
    password2 = fields.Str(required=True)


class UserLogInSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
