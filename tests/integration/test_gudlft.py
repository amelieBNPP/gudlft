from gudlft.db import get_db

def test_database_when_booking(client, app):
    with app.app_context():
        db = get_db()
        club_before_booking = db.execute(
            'SELECT * FROM clubs WHERE name = ?', 
            ('club',),
        ).fetchone()
        competition_before_booking = db.execute(
            'SELECT * FROM competitions WHERE name = ?',
            ('competition',)
        ).fetchone()
    with client:
        response = client.post('/book/competition/club', data={'places': 1})
    with app.app_context():
        db = get_db()
        club_after_booking = db.execute(
            'SELECT * FROM clubs WHERE name = ?', 
            ('club',),
        ).fetchone()
        competition_after_booking = db.execute(
            'SELECT * FROM competitions WHERE name = ?',
            ('competition',)
        ).fetchone()
    assert club_before_booking['points']!=club_after_booking['points']
    assert competition_before_booking['numberOfPlaces']!=competition_after_booking['numberOfPlaces']