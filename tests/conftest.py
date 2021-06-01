import pytest
import uuid

from app.main import app
from app.db.db_engine import init_db, drop_db


@pytest.fixture(scope='module')
def client():
    app.config["TESTING"] = True
    init_db()
    with app.test_client() as client:
        yield client
    drop_db()


@pytest.fixture(scope='module')
def new_user():
    class NewRandomUser:
        def __init__(self):
            self.username = 'test' + str(uuid.uuid1()).replace('-', '')
            self.password = 'pass' + str(uuid.uuid1()).replace('-', '')

        def set_new_password(self, new_password):
            self.password = new_password

    yield NewRandomUser()


@pytest.fixture(scope='module')
def new_user_data(client, new_user):
    client.post('/users', json={
        'username': new_user.username,
        'password1': new_user.password,
        'password2': new_user.password
    })
    yield {'username': new_user.username, 'password': new_user.password}
