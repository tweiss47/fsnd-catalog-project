import click
from datetime import datetime
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


db = SQLAlchemy()


# Database model

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=True)
    provider = db.Column(db.String(64), nullable=False)
    provider_uid = db.Column(db.String(64), nullable=False)

    @property
    def serialize(self):
        return {
            'email': self.email,
            'username': self.username,
            'provider': self.provider,
            'provider_uid': self.provider_uid
        }


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    artist = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    last_update = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    genre = db.relationship(Genre)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'genre': self.genre.name,
            'description': self.description,
            'user_id': self.user.username
        }


# Setup utility commands to initialize the database.

@click.command('init-model')
@with_appcontext
def init_model_command():
    '''Drop database and recreate the schema.'''
    db.drop_all()
    db.create_all()


@click.command('init-test-data')
@with_appcontext
def init_test_data_command():
    '''Add some songs and the list of genres to the database.'''
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

    test_user = User(
        username='Bob',
        email='bob@dobbs.com',
        password=generate_password_hash('welcome'),
        provider='local',
        provider_uid='bob@dobbs.com'
    )
    db.session.add(test_user)

    db.session.add(
        Song(
            title='Across the Tappan Zee',
            genre=genres['Folk'],
            user=test_user,
            artist='Glenn Jones',
            description=(
                "Instrumental for two banjos from the album My Garden State."
            )
        )
    )
    db.session.add(
        Song(
            title='All Day Sucker',
            genre=genres['Soul/R&B'],
            user=test_user,
            artist='Stevie Wonder',
            description=(
                "Masterful funkiness from Stevie Wonder's album Songs in the "
                "Key of Life."
            )
        )
    )
    db.session.add(
        Song(
            title='La Grange',
            genre=genres['Blues'],
            user=test_user,
            artist='ZZ Top',
            description=(
                "From the 1973 album Tres Hombres."
            )
        )
    )
    db.session.add(
        Song(
            title='Little Maggie',
            genre=genres['Folk'],
            user=test_user,
            artist='Robert Plant',
            description=(
                "A reworking of an an Appalacian folk song. From Robert "
                "Plant's 2014 album Lullaby and the Ceasless Roar"
            )
        )
    )
    db.session.commit()


# Simple wrappers for most of the database calls used in the catalog module.
# These were initially mocked before the database model was implemented.

def songs_for(genre):
    g = Genre.query.filter(Genre.name == genre).first()
    return Song.query.filter(Song.genre_id == g.id).order_by(Song.title).all()


def get_genres():
    genres = Genre.query.order_by(Genre.name).all()
    return [n.name for n in genres]


def get_genre(name):
    return Genre.query.filter(Genre.name == name).first()


def get_songs(limit):
    return Song.query.order_by(Song.last_update.desc()).limit(limit)


def get_all_songs():
    return Song.query.order_by(Song.last_update.desc()).all()


def get_song(id):
    return Song.query.filter(Song.id == id).first()
