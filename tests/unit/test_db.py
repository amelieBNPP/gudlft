from gudlft.db import get_db

def test_database_status(app):
    is_database_working = True

    with app.app_context():
        db = get_db()
        try:
            # to check database we will execute raw query
            response = db.execute("SELECT 1 as 'one'").fetchone()
            output = response['one']
        except Exception as e:
            output = str(e)
            is_database_working = False

        assert is_database_working == True
        assert output == 1