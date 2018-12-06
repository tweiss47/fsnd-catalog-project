from flask import (
    Blueprint, render_template
)
from . import model


bp = Blueprint('catalog', __name__)


@bp.route('/')
def index():
    return render_template(
        'catalog/index.html',
        genres=model.get_genres(),
        songs=model.get_songs()
    )


@bp.route('/genre/<path:name>')
def genre_view(name):
    return render_template(
        'catalog/genre_view.html',
        genres=model.get_genres(),
        selected=name,
        songs=model.songs_for(name)
    )


@bp.route('/song/<int:id>')
def song_view(id):
    return render_template(
        'catalog/song_view.html',
        song=model.get_song(id)
    )


@bp.route('/song/add', methods=('GET', 'POST'))
def song_add():
    return 'add a song'


@bp.route('/song/<int:id>/edit', methods=('GET', 'POST'))
def song_edit(id):
    return 'edit a song'


@bp.route('/song/<int:id>/delete', methods=('GET', 'POST'))
def song_delete(id):
    return 'delete a song'
