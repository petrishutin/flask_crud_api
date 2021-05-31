from flask_jwt_extended import JWTManager
from flask import current_app

from app.db.db_engine import Session
from app.db.models import User


def user_identity_lookup(user):
    return user.username


def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = Session.query(User).filter_by(username=identity).one_or_none()
    return user


def check_block_list(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in current_app.config['JWT_BLOCK_LIST']


class JWTAuth(JWTManager):
    """Custom class to avoid decorators and cycle import im main script"""
    def __init__(self, app, **kwargs):
        super(JWTAuth, self).__init__(app)
        self._user_identity_callback = user_identity_lookup
        self._user_lookup_callback = user_lookup_callback
        self._token_in_blocklist_callback = check_block_list
