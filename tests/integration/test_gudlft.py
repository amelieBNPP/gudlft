from tests.conftest import login
from http import HTTPStatus

def test_post_book_ok(client):
    login(client)
    response = client.post('/book/competition/club')
    assert response.status_code==HTTPStatus.OK
    assert "Book" in response.data.decode('utf-8')
    
def test_post_book_ko(client):
    # Competition selected already closed because of past date
    login(client)
    response = client.post('/book/competition_closed/club')
    assert response.status_code==HTTPStatus.OK
    assert "competition_closed" in response.data.decode('utf-8')
    
def test_post_purchase_place_ok(client):
    login(client)
    response = client.post('/book/competition/club')
    assert response.status_code==HTTPStatus.OK
    assert "Book" in response.data.decode('utf-8')
    
def test_club_summary_loggin(client):
    login(client)
    response = client.post('/clubSummary')
    assert response.status_code==HTTPStatus.OK
    assert "Clubs summary" in response.data.decode('utf-8')
    assert "club@gmail.com" in response.data.decode('utf-8')
    
def test_club_summary_loggout(client):
    response = client.post('/clubSummary')
    assert response.status_code==HTTPStatus.OK
    assert "Clubs summary" in response.data.decode('utf-8')
    assert "club@gmail.com" not in response.data.decode('utf-8')
    
def test_purchase_places_OK(client, app):
    PLACES_REQUIRED = 2
    CLUB = 'club'
    COMPETITION = 'competition'
    
    login(client)
    with app.app_context():
        response = client.post(
            '/purchasePlaces', 
            data=dict(
                competition=COMPETITION, 
                club=CLUB,
                places=PLACES_REQUIRED,
            )
        )
    assert response.status_code==HTTPStatus.OK
    assert 'Great-booking complete! You booked 2 places.' in response.data.decode('utf-8')

def test_purchase_places_KO_places(client, app):
    PLACES_REQUIRED = 2
    CLUB = 'club'
    COMPETITION = 'competition_lowPlaces'
    
    login(client)
    with app.app_context():
        response = client.post(
            '/purchasePlaces', 
            data=dict(
                competition=COMPETITION, 
                club=CLUB,
                places=PLACES_REQUIRED,
            )
        )
    assert response.status_code==HTTPStatus.OK
    assert 'Not enought places to book this competition!' in response.data.decode('utf-8')
    
def test_purchase_places_KO_points(client, app):
    PLACES_REQUIRED = 3
    CLUB = 'club'
    COMPETITION = 'competition_new'
    
    login(client)
    with app.app_context():
        response = client.post(
            '/purchasePlaces', 
            data=dict(
                competition=COMPETITION, 
                club=CLUB,
                places=PLACES_REQUIRED,
            )
        )
    print(response.data.decode('utf-8'))
    assert response.status_code==HTTPStatus.OK
    assert 'Not enought points to book this competition!' in response.data.decode('utf-8')