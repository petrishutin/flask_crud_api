def test_swagger_200(client):
    response = client.get('/swagger')
    assert response.status_code == 200


def test_swagger_ui_200(client):
    response = client.get('/swagger-ui')
    assert response.status_code == 200
