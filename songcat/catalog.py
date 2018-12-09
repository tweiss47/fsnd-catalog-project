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
    in_genre = request.args.get('in_genre', '')
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
        genres=model.get_genres(),
        in_genre=in_genre
    )


@bp.route('/song/<int:id>/edit', methods=('GET', 'POST'))
def song_edit(id):
    song = model.get_song(id)

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
        elif song.user.id != g.user.id:
            error = 'Songcat entry owned by {}'.format(song.user_id)
        else:
            genre = model.get_genre(genre_name)
            if genre is None:
                error = 'Unknown genre {}'.format(genre_name)

        if error is None:
            song.title = title
            song.genre = genre
            song.artist = artist
            song.description = description

            model.db.session.add(song)
            model.db.session.commit()

            return redirect(url_for('catalog.index'))

    return render_template(
        'catalog/song_update.html',
        genres=model.get_genres(),
        song=song
    )


@bp.route('/song/<int:id>/delete', methods=('GET', 'POST'))
def song_delete(id):
    if request.method == 'POST':
        song = model.get_song(id)
        model.db.session.delete(song)
        model.db.session.commit()
        return redirect(url_for('catalog.index'))

    return render_template(
        'catalog/song_delete.html',
        song=model.get_song(id)
    )
