from flask import Blueprint, flash, render_template, request
from gudlft.db import get_db
from gudlft import login_required
from gudlft.auth import get_competitions_to_display

bp = Blueprint('api', __name__, url_prefix='/')


@bp.route('/book/<competition>/<club>', methods=('GET', 'POST'))
@login_required
def book(competition,club):
    db = get_db()
    foundClub = db.execute(
            'SELECT * FROM clubs WHERE name=?', (club,)
    ).fetchone()
    foundCompetition = db.execute(
            'SELECT * FROM competitions WHERE name=?', (competition,)
    ).fetchone()
    if foundClub and foundCompetition:
        return render_template('api/booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('api/welcome.html', club=club, competitions=competition)


@bp.route('/purchasePlaces',methods=['POST'])
@login_required
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
    
    opened_competitions, closed_competitions = get_competitions_to_display(db)
    return render_template(
        'api/welcome.html', 
        club=club, 
        opened_competitions=opened_competitions, 
        closed_competitions=closed_competitions,
    )

def update_number_of_places(placesRequired, competition, club):
    db = get_db()
    numberOfPlacesUpdated = int(competition['numberOfPlaces'])-int(placesRequired)
    numberOfPointsUpdated = int(club['points'])-int(placesRequired)
    print(numberOfPlacesUpdated)
    print(numberOfPointsUpdated)
    if numberOfPointsUpdated>0 and numberOfPlacesUpdated>0:
        db.execute(
            "INSERT INTO booking (id_competition, id_club, nbPlaces) VALUES (?,?,?)", (int(competition['id']),int(club['id']),int(placesRequired))
        )
        db.execute(
            'UPDATE competitions SET numberOfPlaces=? WHERE id=?', (int(numberOfPlacesUpdated), int(competition['id']),)
        )
        db.commit()
        db.execute(
            'UPDATE clubs SET points=? WHERE id=?', (int(numberOfPointsUpdated), int(club['id']),)
        )
        db.commit()
        flash('Great-booking complete!')
    elif numberOfPointsUpdated<0:
        flash('Not enought points to book this competition!')
    elif numberOfPlacesUpdated<0:
        flash('Not enought places to book this competition!')
    
