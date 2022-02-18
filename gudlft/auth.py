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
    email=request.form['email']
    db = get_db()
    club = db.execute(
        'SELECT * FROM clubs WHERE email=?', (email,)
    ).fetchone()
    if club:
        competitions = db.execute(
            'SELECT * FROM competitions'    
        )
        session['logged_in'] = True
        return render_template('api/welcome.html',club=club,competitions=competitions)
    else:
        flash("Email unknown")
        return redirect(url_for('auth.index'))