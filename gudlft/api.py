import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from gudlft.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/showSummary',methods=('GET', 'POST'))
def showSummary():
    if request.method == 'POST':
        email = request.form['email']
        db = get_db()
        error = None
        club = db.execute(
            'SELECT * FROM clubs WHERE email = ?', (email,)
        ).fetchone()
        competitions = db.execute(
            'SELECT * FROM competitions'
        )
        return render_template('welcome.html',club=club,competitions=competitions)


@bp.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@bp.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)
