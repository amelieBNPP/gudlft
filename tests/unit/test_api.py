from http import HTTPStatus
from gudlft.api import update_number_of_places, get_clubs, get_competitions, get_booking
from gudlft.auth import get_club_if_auth, get_competitions_to_display
from gudlft.db import get_db
from tests.conftest import login

def test_get_index(client):
    response = client.get('/index')
    assert response.status_code==HTTPStatus.OK
    
def test_get_club_ok(app):
    db = get_db()
    with app.app_context():
        club = get_club_if_auth('club@gmail.com', db)
    assert club['name'] == 'club'

def test_get_club_KO(app):
    db = get_db()
    with app.app_context():
        club = get_club_if_auth('wrongclub@gmail.com', db)
    assert club == None
    
def test_get_competitions(app):
    db = get_db()
    with app.app_context():
        competitions_opened, competition_closed = get_competitions_to_display(db)
    opened = [c['name'] for c in competitions_opened]
    closed = [c['name'] for c in competition_closed]
    assert opened[0] == 'competition'
    assert closed[0] == 'competition_closed'
    
def test_get_booking(app):
    db = get_db()
    with app.app_context():
        booked = get_booking(db, 1, 1)
    assert booked[0]['nbplaces'] == 9

def test_update_places_OK(app):
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


def test_update_places_KO(app):
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

