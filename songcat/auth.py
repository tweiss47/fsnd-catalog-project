from flask import (
    Blueprint, render_template, request, session, redirect, url_for, flash, g
)
from . import model
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('auth', __name__)


@bp.route('/signin', methods=('GET', 'POST'))
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        error = None
        user = model.User.query.filter(model.User.email == email).first()

        if user is None:
            error = 'User is not registered yet.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('catalog.index'))

        flash(error)

    return render_template('auth/signin.html')


@bp.before_app_request
def load_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = model.User.query.filter(model.User.id == user_id).first()


@bp.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('catalog.index'))


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']

        # validate the form input
        error = None
        if email is None:
            error = 'Email is required to register.'
        elif password is None:
            error = 'Password is required to register.'
        else:
            user = model.User.query.filter(model.User.email == email).first()
            if user is not None:
                error = 'User with email {} already registered.'.format(email)

        if error is None:
            # add the new user to the database
            user = model.User(
                email=email,
                password=generate_password_hash(password),
                username=username,
                provider='local'
            )
            model.db.session.add(user)
            model.db.session.commit()

            # add the user to the session
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('catalog.index'))

        flash(error)

    return render_template('auth/register.html')
