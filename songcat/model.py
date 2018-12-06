import click
import datetime
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    artist = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    last_update = db.Column(db.DateTime, onupdate=datetime.datetime.now)

    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    genre = db.relationship(Genre)


@click.command('init-model')
@with_appcontext
def init_model_command():
    db.drop_all()
    db.create_all()


@click.command('add-test-data')
@with_appcontext
def add_test_data():
    genres = {
        'Folk': Genre(name='Folk'),
        'Blues': Genre(name='Blues'),
        'Rock': Genre(name='Rock'),
        'Soul/R&B': Genre(name='Soul/R&B'),
        'Electronic': Genre(name='Electronic'),
        'Pop': Genre(name='Pop'),
        'Country': Genre(name='Country'),
        'Reggae': Genre(name='Reggae'),
    }

    for v in genres.values():
        db.session.add(v)

    db.session.add(
        Song(
            title='Across the Tappan Zee',
            genre=genres['Folk'],
            artist='Glenn Jones',
            description='''
            Instrumental for two banjos from the album My Garden State.
            '''
        )
    )
    db.session.add(
        Song(
            title='All Day Sucker',
            genre=genres['Soul/R&B'],
            artist='Stevie Wonder',
            description='''
            Masterful funkiness from Stevie Wonder's album Songs in the Key
            of Life.
            '''
        )
    )
    db.session.add(
        Song(
            title='La Grange',
            genre=genres['Blues'],
            artist='ZZ Top',
            description='''
            From the 1973 album Tres Hombres.
            '''
        )
    )
    db.session.add(
        Song(
            title='Little Maggie',
            genre=genres['Folk'],
            artist='Robert Plant',
            description='''
            A reworking of an an Appalacian folk song. From Robert Plant's 2014
            album Lullaby and the Ceasless Roar
            '''
        )
    )
    db.session.commit()


def songs_for(genre):
    g = Genre.query.filter(Genre.name == genre).first()
    return Song.query.filter(Song.genre_id == g.id).order_by(Song.title).all()


def get_genres():
    genres = Genre.query.order_by(Genre.name).all()
    return [n.name for n in genres]


def get_songs():
    return Song.query.order_by(Song.last_update.desc())[:10]


def get_song(id):
    return Song.query.filter(Song.id == id).first()
