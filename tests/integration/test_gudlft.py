from gudlft.db import get_db
from tests.conftest import login
from http import HTTPStatus

def test_database_when_booking(client, app):
    pass
    # login(client)
    # with client:
    #     response = client.post('/book/competition/club')
    # assert response.status_code==HTTPStatus.FOUND
    # print(response.data)
    # with client:
    #     response = client.post('/purchasePlaces', data={'places':1})
    # print(response.data)
    # assert 1!=1