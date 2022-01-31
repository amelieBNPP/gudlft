import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import json


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    for club in loadClubs():
        db.execute(
            "INSERT INTO clubs (username, email, points) VALUES (?,?,?)",(club['name'],club['email'],club['points'])
        )
    for competition in loadCompetitions():
        db.execute(
            "INSERT INTO competitions (name, date, numberOfPlaces) VALUES (?,?,?)",(competition['name'],competition['date'],competition['numberOfPlaces'])
        )

def loadClubs():
    with open('gudlft/json/clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('gudlft/json/competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
    
def init_app(app):
    # tells Flask to call that function when cleaning up after returning the response.
    app.teardown_appcontext(close_db)
    # adds a new command that can be called with the flask command.
    app.cli.add_command(init_db_command)
    

