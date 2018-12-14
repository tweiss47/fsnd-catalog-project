from flask import (
    Blueprint, render_template, request, session, redirect, url_for, flash, g,
    make_response
)
from werkzeug.security import (
    check_password_hash, generate_password_hash, hashlib
)
from werkzeug.exceptions import BadRequest
from google.oauth2 import id_token
from google.auth.transport import requests
from os import urandom
import functools
import json
from . import model


bp = Blueprint('auth', __name__)


@bp.route('/signin', methods=('GET', 'POST'))
def signin():
    if request.method == 'POST':
        # POST request on the sign in form implements local login.
        validate_csrf_token()

        # Gather form data.
        email = request.form['email']
        password = request.form['password']

        # Validate input.
        error = None
        user = model.User.query.filter(
            model.User.provider_uid == email
        ).first()

        if user is None:
            error = 'User is not registered yet.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        # Set session state to indicate the logged in user.
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('catalog.index'))

        flash(error)

    state = hashlib.sha256(urandom(1024)).hexdigest()
    session['state'] = state
    return render_template('auth/signin.html', state=state)


@bp.before_app_request
def load_user():
    # Ensure the user object is available if the user is signed in.
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = model.User.query.filter(model.User.id == user_id).first()

    # Add the google client id to the request context
    g.google_client_id = GOOGLE_CLIENT_ID


@bp.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('catalog.index'))


@bp.route('/register', methods=('GET', 'POST'))
def register():
    # Register a new local user.
    if request.method == 'POST':
        # Gather form data.
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']

        # Validate the form input.
        error = None
        if email is None:
            error = 'Email is required to register.'
        elif password is None:
            error = 'Password is required to register.'
        else:
            user = model.User.query.filter(
                model.User.provider_uid == email
            ).first()
            if user is not None:
                error = 'User with email {} already registered.'.format(email)

        if error is None:
            # Add the new user to the database.
            user = model.User(
                email=email,
                password=generate_password_hash(password),
                username=username,
                provider='local',
                provider_uid=email
            )
            model.db.session.add(user)
            model.db.session.commit()

            # Add the user to the session.
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('catalog.index'))

        # Report errors before rendering if the POST fails.
        flash(error)

    return render_template('auth/register.html')


# Support the google auth provider. Will need to make this more generic
# if other providers are supported in the future.

GOOGLE_CLIENT_ID = (
    '608830178668-2mdo879m5gltao8eqa1s80bd52ot8d3m'
    '.apps.googleusercontent.com'
)


@bp.route('/gconnect', methods=('POST', ))
def gconnect():
    # Check client CSRF token.
    validate_csrf_token()

    # Get the id token from the request.
    token = request.form.get('id_token', None)
    if token is None:
        response = make_response(
            json.dumps('No id_token value was passed'), 400
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    try:
        # Validate the token.
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        if idinfo['iss'] not in [
            'accounts.google.com', 'https://accounts.google.com'
        ]:
            raise ValueError('Wrong issuer.')

    except ValueError:
        # Token validation failure.
        response = make_response(
            json.dumps('ValueError raised during token validation'), 500
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    # Save the user info if the user is new
    user_id = idinfo['sub']
    user = model.User.query.filter(
        model.User.provider == 'google' and model.User.provider_uid == user_id
    ).first()
    if user is None:
        user = model.User(
            provider='google',
            email=idinfo['email'],
            username=idinfo['given_name'],
            provider_uid=user_id
        )
        model.db.session.add(user)
        model.db.session.commit()

    # Save the user session
    session.clear()
    session['user_id'] = user.id

    # Return a serialized user object
    response = make_response(json.dumps(user.serialize), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


def validate_csrf_token():
    # check to see if a valid state parameter was submitted on POST
    state = request.form.get('state', None)
    if state is None or state != session['state']:
        raise BadRequest('Invalid form submision.')


def signin_required(view):
    # decorator that enforces sign in for views that require auth
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.signin'))
        return view(**kwargs)

    return wrapped_view
