import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from gudlft.db import get_db

bp = Blueprint('api', __name__, url_prefix='/')


@bp.route('/showSummary', methods=('GET', 'POST'))
def showSummary():
    if request.method == 'POST':
        email = request.form['email']
        db = get_db()
        club = db.execute(
            'SELECT * FROM clubs WHERE email=?', (email,)
        ).fetchone()
        competitions = db.execute(
            'SELECT * FROM competitions'
        )
        return render_template('api/welcome.html',club=club,competitions=competitions)
    return render_template('api/showSummary.html')


@bp.route('/book/<competition>/<club>', methods=('GET', 'POST'))
def book(competition,club):
    db = get_db()
    foundClub = db.execute(
            'SELECT * FROM clubs WHERE name=?', (club,)
    ).fetchone()
    foundCompetition = db.execute(
            'SELECT * FROM competitions WHERE name=?', (competition,)
    ).fetchone()
    if foundClub and foundCompetition:
        print("Done")
        return render_template('api/booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('api/welcome.html', club=club, competitions=competition)


@bp.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    db = get_db()
    competition = request.form['competition']
    club = request.form['club']
    competitions = db.execute(
            'SELECT * FROM competitions',
    ).fetchall()
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    clubs = db.execute(
            'SELECT * FROM clubs'
    ).fetchall()
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    update_number_of_places(request.form['places'], competition, club)
    
    competitions = db.execute(
            'SELECT * FROM competitions',
    ).fetchall()
    club = db.execute(
            'SELECT * FROM clubs WHERE name=?',(request.form['club'],)
    ).fetchone()
    return render_template('api/welcome.html', club=club, competitions=competitions)

def update_number_of_places(placesRequired, competition, club):
    db = get_db()
    numberOfPlacesUpdated = int(competition['numberOfPlaces'])-int(placesRequired)
    numberOfPointsUpdated = int(club['points'])-int(placesRequired)
    db.execute(
        'UPDATE competitions SET numberOfPlaces=? WHERE name=?', (int(numberOfPlacesUpdated), str(competition),)
    )
    db.execute(
        'UPDATE clubs SET points=? WHERE name=?', (int(numberOfPlacesUpdated), str(club),)
    )
    db.commit()
    flash('Great-booking complete!')
