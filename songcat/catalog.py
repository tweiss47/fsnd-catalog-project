from flask import (
    Blueprint, render_template, request, flash, redirect, url_for, g
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
    if request.method == 'POST':
        title = request.form.get('title')
        genre_name = request.form.get('genre')
        artist = request.form.get('artist')
        description = request.form.get('description')

        error = None
        if title is None:
            error = 'Title is required.'
        elif genre_name is None:
            error = 'Genre is required.'
        elif artist is None:
            error = 'Artist is required.'
        else:
            genre = model.get_genre(genre_name)
            if genre is None:
                error = 'Unknown genre {}'.format(genre_name)

        if error is None:
            song = model.Song(
                title=title,
                genre=genre,
                artist=artist,
                description=description,
                user=g.user
            )
            model.db.session.add(song)
            model.db.session.commit()
            return redirect(url_for('catalog.index'))

        flash(error)

    return render_template(
        'catalog/song_add.html',
        genres=model.get_genres()
    )


@bp.route('/song/<int:id>/edit', methods=('GET', 'POST'))
def song_edit(id):
    return 'edit a song'


@bp.route('/song/<int:id>/delete', methods=('GET', 'POST'))
def song_delete(id):
    return 'delete a song'
