import pytest


@pytest.fixture(scope='module')
def access_token(client, new_user_data):
    response = client.post('/login', json=new_user_data)
    return response.json['access_token']


def test_post_todo_201(client, access_token, new_user, request):
    response = client.post(
        f'/todos/{new_user.username}',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'text': 'some text', 'status': 'TODO'}
    )
    assert response.status_code == 201
    todo_id = response.json['result']
    assert isinstance(todo_id, int)
    request.config.cache.set('todo_id', todo_id)


def test_post_invalid_status_422(client, access_token, new_user):
    response = client.post(
        f'/todos/{new_user.username}',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'text': 'some text', 'status': 'ARRIVED'}
    )
    assert response.status_code == 422


def test_get_todo_by_id_200(client, access_token, new_user, request):
    todo_id = request.config.cache.get('todo_id', None)
    response = client.get(
        f'/todos/{new_user.username}/{todo_id}',
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert response.status_code == 200
    assert response.json['id'] == todo_id


def test_get_all_todos_200(client, access_token, new_user):
    response = client.get(
        f'/todos/{new_user.username}',
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_unauthorized_get_all_todos_401(client, access_token, new_user):
    other_user = 'other_user'
    response = client.get(
        f'/todos/{other_user}',
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert response.status_code == 401
    assert response.json['message'] == f"User {new_user.username} not authorized to get resource /todos/{other_user}"


def test_put_todo_202(client, access_token, new_user, request):
    todo_id = request.config.cache.get('todo_id', None)
    response = client.put(
        f'/todos/{new_user.username}/{todo_id}',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'text': 'some text more', 'status': 'DONE'}
    )
    assert response.status_code == 202
    assert response.json == {'result': f'Todo id:{todo_id} successfully updated!'}


def test_delete_todo_by_id_200(client, access_token, new_user, request):
    todo_id = request.config.cache.get('todo_id', None)
    response = client.delete(
        f'/todos/{new_user.username}/{todo_id}',
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert response.status_code == 200
    assert response.json == {'result': f'Todo id:{todo_id} successfully deleted!'}
