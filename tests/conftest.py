import os
import tempfile

import pytest

from gudlft import create_app
from gudlft.db import init_db, get_db
    
MOCK_CLUBS = "INSERT INTO clubs (name, email, points) VALUES ('club', 'club@gmail.com', 8)"
MOCK_COMPETITIONS = "INSERT INTO competitions (name, date, numberOfPlaces) VALUES ('competition', '2023-02-16 00:00:00', 25)"
MOCK_COMPETITIONS_CLOSED = "INSERT INTO competitions (name, date, numberOfPlaces) VALUES ('competition_closed', '2021-02-16 00:00:00', 25)"
MOCK_COMPETITIONS_LOWPLACES = "INSERT INTO competitions (name, date, numberOfPlaces) VALUES ('competition_lowPlaces', '2022-07-21 00:00:00', 1)"
MOCK_COMPETITIONS_NEW = "INSERT INTO competitions (name, date, numberOfPlaces) VALUES ('competition_new', '2022-07-21 00:00:00', 25)"
MOCK_BOOKING = "INSERT INTO booking (id_competition, id_club, nbPlaces) VALUES (1, 1, 9)"

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })
    
    with app.app_context():
            init_db()
            db = get_db()
            db.executescript(MOCK_CLUBS)
            db.executescript(MOCK_COMPETITIONS)
            db.executescript(MOCK_COMPETITIONS_CLOSED)
            db.executescript(MOCK_COMPETITIONS_LOWPLACES)
            db.executescript(MOCK_BOOKING)
            db.executescript(MOCK_COMPETITIONS_NEW)
    
    yield app
    
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


def login(client):
    return client.post(
        '/showSummary', 
        data=dict(email='club@gmail.com'),
    )
