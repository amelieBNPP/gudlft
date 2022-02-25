from http import HTTPStatus
from tests.conftest import login
from flask import session

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
    
def test_log_out(client, app):
    login(client)
    with client:
        response = client.post('/logout')
    assert response.status_code==HTTPStatus.FOUND
    assert response.headers['Location']=='http://localhost/index'