from http import HTTPStatus
import logging
from gudlft.api import update_number_of_places, get_clubs, get_competitions, get_booking
from gudlft.db import get_db
from tests.conftest import login
from flask import session

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

def test_update_places_OK(client, app):
    PLACES_REQUIRED = 2
    CLUB = 'club'
    COMPETITION = 'competition'
    with app.app_context():
        db = get_db()

        club_before_booking = get_clubs(db, CLUB)
        competition_before_booking = get_competitions(db, COMPETITION)

        update_number_of_places(db, PLACES_REQUIRED, competition_before_booking, club_before_booking)

        club_after_booking = get_clubs(db, CLUB)
        competition_after_booking = get_competitions(db, COMPETITION)
    assert club_before_booking['points']==(club_after_booking['points'] + (PLACES_REQUIRED*3))
    assert competition_before_booking['numberOfPlaces']==(competition_after_booking['numberOfPlaces'] + PLACES_REQUIRED)


def test_update_places_KO(client, app):
    # MOE than 12 places booked
    PLACES_REQUIRED = 4
    CLUB = 'club'
    COMPETITION = 'competition'
    with app.app_context():
        db = get_db()

        club_before_booking = get_clubs(db, CLUB)
        competition_before_booking = get_competitions(db, COMPETITION)

        update_number_of_places(db, PLACES_REQUIRED, competition_before_booking, club_before_booking)

        club_after_booking = get_clubs(db, CLUB)
        competition_after_booking = get_competitions(db, COMPETITION)

    assert club_before_booking['points']==club_after_booking['points']
    assert competition_before_booking['numberOfPlaces']==competition_after_booking['numberOfPlaces']

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