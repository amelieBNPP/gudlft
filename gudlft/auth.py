import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from gudlft.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/')


@bp.route('/index', methods=('GET', 'POST'))
def index():
    print(request.method)
    if request.method == 'POST':
        email = request.form['email']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM clubs WHERE email = ?', (email,)
        ).fetchone()
        return redirect(url_for('api.show_summary'))
        # if user is None:
        #     error = 'Unknown email.'
        # print(error)
        # if error is None:
        #     print(error)
        #     session.clear()
        #     session['user_id'] = user['id']
        #     return redirect(url_for('api.show_summary'))

        # flash(error)

    return render_template('auth/index.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        
@bp.route('/logout')
def logout():
    """To log out, you need to remove the user id from the session."""
    session.clear()
    return redirect(url_for('auth.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        """ This decorator checks if a user is loaded and redirects to the login page otherwise. 
        If a user is loaded the original view is called and continues normally. """
        if g.user is None:
            return redirect(url_for('auth.index'))

        return view(**kwargs)

    return wrapped_view