import logging

from werkzeug.exceptions import BadRequest, InternalServerError, NotFound

from app.db.db_engine import Session
from app.db.models import User, ToDo

logger = logging.getLogger(__name__)


def user_does_exists(username: str) -> bool:
    return bool(Session.query(User).filter_by(username=username).one_or_none())


def get_user_instance(username: str, password: str) -> User:
    user = Session.query(User).filter_by(username=username).one_or_none()
    if not user:
        raise NotFound(f'User {username} not found')
    if user.password != User.hash_password(password):
        raise BadRequest('invalid password')
    return user


def create_user(username: str, password: str):
    new_user = User(username, password)
    Session.add(new_user)
    try:
        Session.commit()
    except Exception as e:
        logger.error(f'Can not write new user to DB: {e}')
        raise InternalServerError('Can not create user')


def update_user_password(user: User, password):
    user.password = password
    try:
        Session.commit()
    except Exception as e:
        logger.error(f'Can not update record in DB: {e}')
        raise InternalServerError('Can not update user password')


def create_new_todo(username: str, text: str, status: str) -> int:
    new_todo = ToDo(user_name=username, text=text, status=status)
    Session.add(new_todo)
    try:
        Session.commit()
    except Exception as e:
        logger.error(f'Can not write new todo to DB: {e}')
        raise InternalServerError('Can not create new todo')
    return new_todo.id


def get_todos(username):
    """get all todos"""
    try:
        todos = Session.query(ToDo).filter_by(user_name=username).all()
    except Exception as e:
        logger.error(f'Can get todos from DB: {e}')
        raise InternalServerError(f'Can get todos for {username}')
    result = []
    for todo in todos:
        result.append({
            'id': todo.id, 'text': todo.text, 'status': todo.status,
            'create_time': todo.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': todo.update_time.strftime('%Y-%m-%d %H:%M:%S')
        })
    return result


def get_todo_instance(username: str, todo_id: str) -> ToDo:
    try:
        todo = Session.query(ToDo).filter_by(user_name=username).filter_by(
            id=todo_id).one_or_none()
    except Exception as e:
        logger.error(f'Can get todos from DB: {e}')
        raise InternalServerError(f'Can not get todo {todo_id} for {username}')
    if not todo:
        raise NotFound(f'todo id#:{todo_id} not found')
    return todo


def get_todo(username: str, todo_id: str):
    """get all todos"""
    todo = get_todo_instance(username, todo_id)
    return {
        'id': todo.id, 'text': todo.text, 'status': todo.status,
        'create_time': todo.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        'update_time': todo.update_time.strftime('%Y-%m-%d %H:%M:%S')
    }


def update_todo(username: str, todo_id: str, text=None, status=None):
    todo = get_todo_instance(username, todo_id)
    if not text and not status:
        raise BadRequest('Nothing to update')
    if text:
        todo.text = text
    if status:
        todo.status = status
    try:
        Session.commit()
    except Exception as e:
        logger.error(f'Can not update record in DB: {e}')
        raise InternalServerError(f'Can not update todo {todo_id}')
    Session.refresh(todo)
    return todo


def delete_todo(username: str, todo_id: str):
    todo = get_todo_instance(username, todo_id)
    try:
        Session.delete(todo)
        Session.commit()
    except Exception as e:
        logger.error(f'Can not delete record in DB: {e}')
        raise InternalServerError(f'Can not delete todo {todo_id}')
