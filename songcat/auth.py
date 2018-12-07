from flask import (
    Blueprint, render_template
)


bp = Blueprint('auth', __name__)


@bp.route('/signin')
def signin():
    return render_template('auth/signin.html')


@bp.route('/signout')
def signout():
    return 'signout'


@bp.route('/register')
def register():
    return render_template('auth/register.html')
