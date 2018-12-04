from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


bp = Blueprint('auth', __name__)


@bp.route('/signin')
def signin():
    return 'signin'


@bp.route('/signout')
def signout():
    return 'signout'


@bp.route('/register')
def register():
    return 'register'

