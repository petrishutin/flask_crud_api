def test_post_new_user_200(new_user, client):
    data = {
        'username': new_user.username,
        'password1': new_user.password,
        'password2': new_user.password
    }
    response = client.post('/users', json=data)
    assert response.status_code == 201, response.data


def test_post_passwords_mismatch_422(new_user, client):
    data = {
        'username': new_user.username,
        'password1': new_user.password,
        'password2': new_user.password + '1'
    }
    response = client.post('/users', json=data)
    assert response.status_code == 422, response.data


def test_change_password_200(new_user, client):
    data = {
        'username': new_user.username,
        'old_password': new_user.password,
        'password1': new_user.password + '1',
        'password2': new_user.password + '1'
    }
    response = client.put('/users', json=data)
    assert response.status_code == 202
