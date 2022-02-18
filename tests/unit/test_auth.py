from http import HTTPStatus

def test_get_auth(client):
    response = client.get('/index')
    assert response.status_code==HTTPStatus.OK

def test_post_auth_OK(client):
    response = client.post( 
        '/showSummary', 
        data=dict(email='club@gmail.com'),
    )
    assert response.status_code==HTTPStatus.OK
    assert 'club@gmail.com' in response.get_data(as_text=True)

def test_post_auth_KO(client):
    response = client.post(
        '/showSummary', 
        data=dict(email='wrongclub@gmail.com'),
    )
    assert response.status_code==HTTPStatus.FOUND
    assert response.headers['Location']=='http://localhost/index'