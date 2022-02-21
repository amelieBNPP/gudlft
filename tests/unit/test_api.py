from http import HTTPStatus
import logging
from gudlft.api import update_number_of_places
from gudlft.db import get_db
from tests.conftest import login
from flask import session

def test_post_book_ok(client):
    login(client)
    response = client.post('/book/competition/club')
    assert response.status_code==HTTPStatus.OK
    assert "Book" in response.data.decode('utf-8')
    
def test_post_book_ko(client):
    login(client)
    response = client.post('/book/competition_closed/club')
    assert response.status_code==HTTPStatus.OK
    assert "competition_closed" in response.data.decode('utf-8')

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

    