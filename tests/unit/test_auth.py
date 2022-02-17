from http import HTTPStatus

def test_get_auth(client):
    response = client.get('/index')
    assert response.status_code==HTTPStatus.OK
    
def test_post_auth(client):
    response = client.post(
        '/index', 
        data=dict(email='john@simplylift.co'),
    )
    assert response.status_code==HTTPStatus.FOUND