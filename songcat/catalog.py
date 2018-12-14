from flask import (
    Blueprint, render_template, request, flash, redirect, url_for, g
)
from songcat.model import (
    get_genres, get_songs, songs_for, get_song, get_genre, Song, db
)
from songcat.auth import signin_required


bp = Blueprint('catalog', __name__)


@bp.route('/')
def index():
    return render_template(
        'catalog/index.html',
        genres=get_genres(),
        songs=get_songs(10)
    )


@bp.route('/genre/<path:name>')
def genre_view(name):
    return render_template(
        'catalog/genre_view.html',
        genres=get_genres(),
        selected=name,
        songs=songs_for(name)
    )


@bp.route('/song/<int:id>')
def song_view(id):
    return render_template(
        'catalog/song_view.html',
        song=get_song(id)
    )


@bp.route('/song/add', methods=('GET', 'POST'))
@signin_required
def song_add():
    # When invoked from the genre view in_genre is passed as a parameter
    in_genre = request.args.get('in_genre', '')
    if request.method == 'POST':
        # Gather form input.
        title = request.form.get('title')
        genre_name = request.form.get('genre')
        artist = request.form.get('artist')
        description = request.form.get('description')

        # Validate the input.
        error = None
        if title is None:
            error = 'Title is required.'
        elif genre_name is None:
            error = 'Genre is required.'
        elif artist is None:
            error = 'Artist is required.'
        else:
            genre = get_genre(genre_name)
            if genre is None:
                error = 'Unknown genre {}'.format(genre_name)

        # Commit the new song.
        if error is None:
            song = Song(
                title=title,
                genre=genre,
                artist=artist,
                description=description,
                user=g.user
            )
            db.session.add(song)
            db.session.commit()
            return redirect(url_for('catalog.index'))

        # Report error when rendering rendering after a POST attempt.
        flash(error)

    return render_template(
        'catalog/song_add.html',
        genres=get_genres(),
        in_genre=in_genre
    )


@bp.route('/song/<int:id>/edit', methods=('GET', 'POST'))
@signin_required
def song_edit(id):
    song = get_song(id)

    if request.method == 'POST':
        # Gather form input.
        title = request.form.get('title')
        genre_name = request.form.get('genre')
        artist = request.form.get('artist')
        description = request.form.get('description')

        # Validate input.
        error = None
        if title is None:
            error = 'Title is required.'
        elif genre_name is None:
            error = 'Genre is required.'
        elif artist is None:
            error = 'Artist is required.'
        elif song.user.id != g.user.id:
            error = 'Songcat entry owned by {}'.format(song.user.username)
        else:
            genre = get_genre(genre_name)
            if genre is None:
                error = 'Unknown genre {}'.format(genre_name)

        # Update the database.
        if error is None:
            song.title = title
            song.genre = genre
            song.artist = artist
            song.description = description

            db.session.add(song)
            db.session.commit()

            return redirect(url_for('catalog.index'))

        # Report error when rendering rendering after a POST attempt.
        flash(error)

    return render_template(
        'catalog/song_update.html',
        genres=get_genres(),
        song=song
    )


@bp.route('/song/<int:id>/delete', methods=('GET', 'POST'))
@signin_required
def song_delete(id):
    if request.method == 'POST':
        song = get_song(id)

        # Validate that the user owns the song
        error = None
        if song.user_id != g.user.id:
            error = 'Songcat entry owned by {}'.format(song.user.username)

        if error is None:
            db.session.delete(song)
            db.session.commit()
            return redirect(url_for('catalog.index'))

        # Report errors before rendering on an invalid post
        flash(error)

    return render_template(
        'catalog/song_delete.html',
        song=get_song(id)
    )
