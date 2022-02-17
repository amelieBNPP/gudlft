import os
import tempfile

import pytest

from gudlft import create_app
from gudlft.db import init_db, get_db
    
MOCK_CLUBS = "INSERT INTO clubs (name, email, points) VALUES ('club', 'club@gmail.com', 4)"
MOCK_COMPETITIONS = "INSERT INTO competitions (name, date, numberOfPlaces) VALUES ('competition', '2022-02-16 00:00:00', 25)"

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
    
    yield app
    
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


def login(client):
    return client.post(
        '/index', 
        data=dict(email='club@gmail.com'),
    )
