import pytest
import uuid
import random
import string

from app.db.models import User
from app.main import app
from app.db.db_engine import init_db, Session


@pytest.fixture(scope='module')
def client():
    app.config["TESTING"] = True
    init_db()
    with app.test_client() as client:
        yield client


class NewRandomUser:
    def __init__(self):
        self.username = 'test' + str(uuid.uuid1())
        self.password = ''.join(random.choice(string.ascii_letters) for i in range(6))

    def set_new_password(self, new_password):
        self.password = new_password


@pytest.fixture(scope='class')
def random_user():
    user = NewRandomUser()
    yield user
    user_to_delete = Session.query(User).filter_by(username=user.username).first()
    Session.delete(user_to_delete)
    Session.commit()
    Session.close()


class TestUser:
    def test_post_new_user_200(self, random_user, client):
        data = {
            'username': random_user.username,
            'password1': random_user.password,
            'password2': random_user.password
        }
        response = client.post('/users', json=data)
        assert response.status_code == 201, response.data

    def test_change_password_200(self, random_user, client):
        data = {
            'username': random_user.username,
            'old_password': random_user.password,
            'password1': random_user.password + '1',
            'password2': random_user.password + '1'
        }
        response = client.put('/users', json=data)
        assert response.status_code == 202
