from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . import model


bp = Blueprint('catalog', __name__)


@bp.route('/')
def index():
    genres = [
        'Blues', 'Classical', 'Jazz', 'Reggae', 'Country',
        'Electronic', 'Folk', 'Rock', 'Soul/R&B'
    ]
    songs = [
        model.Song(1, 'Across the Tappan Zee', 'Folk'),
        model.Song(2, 'All Day Sucker', 'Soul/R&B'),
        model.Song(3, 'La Grange', 'Blues'),
        model.Song(4, 'Little Maggie', 'Folk')
    ]
    return render_template('catalog/index.html', genres=genres, songs=songs)


@bp.route('/genre/<path:name>')
def genre_view(name):
    return 'genre view for {}'.format(name)


@bp.route('/song/<int:id>')
def song_view(id):
    return 'song view for {}'.format(id)


@bp.route('/song/add', methods=('GET', 'POST'))
def song_add():
    return 'add a song'


@bp.route('/song/<int:id>/edit', methods=('GET', 'POST'))
def song_edit(id):
    return 'edit a song'


@bp.route('/song/<int:id>/delete', methods=('GET', 'POST'))
def song_delete(id):
    return 'delete a song'

