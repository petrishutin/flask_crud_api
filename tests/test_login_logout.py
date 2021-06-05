def test_post_login_200(client, new_user_data, request):
    response = client.post('/login', json=new_user_data)
    assert response.status_code == 200, response.data
    assert 'access_token' in response.json
    assert response.json['access_token']
    request.config.cache.set('access_token', response.json['access_token'])


def test_post_logout_200(client, request):
    access_token = request.config.cache.get('access_token', None)
    response = client.get('/logout', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.get_json()['result'] == 'Token revoked'


def test_post_log_out_again_400(client, request):
    access_token = request.config.cache.get('access_token', None)
    response = client.get('/logout', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 401
    assert response.get_json()['msg'] == 'Token has been revoked'
