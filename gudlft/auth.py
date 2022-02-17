from flask import (
    Blueprint, redirect, render_template, request, session, url_for
)

from gudlft.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/')


@bp.route('/index', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        email = request.form['email']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM clubs WHERE email = ?', (email,)
        ).fetchone()
        return redirect(url_for('api.showSummary'))

    return render_template('auth/index.html')

        
@bp.route('/logout')
def logout():
    """To log out, you need to remove the user id from the session."""
    session.clear()
    return redirect(url_for('auth.index'))