from flask import (
    Blueprint, redirect, render_template, request, session, url_for, flash
)
from gudlft.db import get_db
from gudlft import login_required


bp = Blueprint('auth', __name__, url_prefix='/')


@bp.route('/index', methods=('GET', 'POST'))
def index():
    return render_template('auth/index.html')
        
@bp.route('/logout')
@login_required
def logout():
    """To log out, you need to remove the user id from the session."""
    session.clear()
    return redirect(url_for('auth.index'))

@bp.route('/showSummary', methods=('GET', 'POST'))
def showSummary():
    db = get_db()
    club = get_club_if_auth(request.form['email'], db)
    if club:
        opened_competitions, closed_competitions = get_competitions_to_display(db)

        session['logged_in'] = True
        session['email'] = club['email']
        return render_template(
            'api/welcome.html',
            club=club,
            opened_competitions=opened_competitions,
            closed_competitions=closed_competitions,
        )
    else:
        flash("Email unknown")
        return redirect(url_for('auth.index'))
    
def get_club_if_auth(email, db):
    return db.execute(
        'SELECT * FROM clubs WHERE email=?', (email,)
    ).fetchone()

def get_competitions_to_display(db):
    opened_competitions = db.execute(
            'SELECT * FROM competitions WHERE date(date)>date("now")'    
        )
    closed_competitions = db.execute(
            'SELECT * FROM competitions WHERE date(date)<date("now")'    
        )
    return opened_competitions, closed_competitions
