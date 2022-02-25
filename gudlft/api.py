import email
from flask import Blueprint, flash, render_template, request, session
from gudlft.db import get_db
from gudlft import login_required
from gudlft.auth import get_competitions_to_display

bp = Blueprint('api', __name__, url_prefix='/')


@bp.route('/clubSummary', methods=('GET', 'POST'))
def clubSummary():
    """To display clubs summary."""
    db = get_db()
    clubs = get_clubs(db)
    email = None if session=={} else session['email']
    return render_template('api/summary.html', clubs=clubs, email=email)

@bp.route('/book/<competition>/<club>', methods=('GET', 'POST'))
@login_required
def book(competition,club):
    db = get_db()
    foundClub = get_clubs(db, club)
    foundCompetition = get_competitions(db, competition)

    if foundClub and foundCompetition:
        return render_template('api/booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('api/welcome.html', club=club, competitions=competition)


@bp.route('/purchasePlaces',methods=['POST'])
@login_required
def purchasePlaces():
    db = get_db()
    
    competition = get_competitions(db,request.form['competition'])
    
    club = get_clubs(db, request.form['club'])
    
    update_number_of_places(db, request.form['places'], competition, club)
    
    club = get_clubs(db, request.form['club'])
    opened_competitions, closed_competitions = get_competitions_to_display(db)

    return render_template(
        'api/welcome.html', 
        club=club, 
        opened_competitions=opened_competitions, 
        closed_competitions=closed_competitions,
    )

def update_number_of_places(db, placesRequired, competition, club):
    numberOfPlacesUpdated = int(competition['numberOfPlaces'])-int(placesRequired)
    numberOfPointsUpdated = int(club['points'])-(int(placesRequired)*3)
    numberOfPlaceAvailable = 12

    booking = get_booking(db, competition['id'], club['id'])

    if booking:
        numberOfPlaceAvailable = 12 - sum([book['nbPlaces'] for book in booking]) - int(placesRequired)
        
    if numberOfPointsUpdated>0 and numberOfPlacesUpdated>0 and numberOfPlaceAvailable>0:
        db.execute(
            "INSERT INTO booking (id_competition, id_club, nbPlaces) VALUES (?,?,?)", (int(competition['id']),int(club['id']),int(placesRequired))
        )
        db.execute(
            'UPDATE competitions SET numberOfPlaces=? WHERE id=?', (int(numberOfPlacesUpdated), int(competition['id']),)
        )
        db.execute(
            'UPDATE clubs SET points=? WHERE id=?', (int(numberOfPointsUpdated), int(club['id']),)
        )
        db.commit()
        flash('Great-booking complete!')
    elif numberOfPlaceAvailable<=0:
        flash('You already booked more than 12 places!')
    elif numberOfPointsUpdated<0:
        flash('Not enought points to book this competition!')
    elif numberOfPlacesUpdated<0:
        flash('Not enought places to book this competition!')
    
def get_clubs(db, name=None):
    if name:
        return db.execute(
            'SELECT * FROM clubs WHERE name=?', (name,)
        ).fetchone()
    return db.execute(
            'SELECT * FROM clubs'
    ).fetchall()
    
def get_competitions(db, name=None):
    if name:
        return db.execute(
            'SELECT * FROM competitions WHERE name=?', (name,)
        ).fetchone()
    return db.execute(
            'SELECT * FROM competitions',
    ).fetchall()
    
def get_booking(db, id_competition=None, id_club=None):
    return  db.execute(
        "SELECT * FROM booking WHERE id_competition=? AND id_club=?", (int(id_competition), int(id_club))
    ).fetchall()