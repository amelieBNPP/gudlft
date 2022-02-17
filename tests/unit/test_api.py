from tests.conftest import login
from http import HTTPStatus
from gudlft.api import update_number_of_places
from gudlft.db import get_db

def test_get_showSummary(client):
    response = login(client)
    assert response.headers['Location']=='http://localhost/showSummary'
    
def test_post_book_ok(client):
    with client:
        response = client.post('/book/competition/club', data={'places': 1})
    assert response.status_code==HTTPStatus.OK
    
def test_update_places(client, app):
    PLACES_REQUIRED = 2
    CLUB = 'club'
    COMPETITION = 'competition'
    with app.app_context():
        db = get_db()
        club_before_booking = db.execute(
            'SELECT * FROM clubs WHERE name = ?', 
            (CLUB,),
        ).fetchone()
        competition_before_booking = db.execute(
            'SELECT * FROM competitions WHERE name = ?',
            (COMPETITION,)
        ).fetchone()
    update_number_of_places(PLACES_REQUIRED, competition_before_booking, club_before_booking)
    with app.app_context():
        db = get_db()
        club_after_booking = db.execute(
            'SELECT * FROM clubs WHERE name = ?', 
            (CLUB,),
        ).fetchone()
        competition_after_booking = db.execute(
            'SELECT * FROM competitions WHERE name = ?',
            (COMPETITION,)
        ).fetchone()
    assert club_before_booking['points']!=club_after_booking['points']
    assert competition_before_booking['numberOfPlaces']!=competition_after_booking['numberOfPlaces'] 

    