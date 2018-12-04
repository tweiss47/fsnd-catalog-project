from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


bp = Blueprint('catalog', __name__)


@bp.route('/')
def index():
    return render_template('base.html')


@bp.route('/genre/<name>')
def genre(name):
    return 'genre index'


@bp.route('/song/<int:id>')
def song_view(id):
    return 'song view'


@bp.route('/song/add', methods=('GET', 'POST'))
def song_add():
    return 'add a song'


@bp.route('/song/<int:id>/edit', methods=('GET', 'POST'))
def song_edit(id):
    return 'edit a song'


@bp.route('/song/<int:id>/delete', methods=('GET', 'POST'))
def song_delete(id):
    return 'delete a song'

