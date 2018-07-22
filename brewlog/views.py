from flask import render_template, request, redirect
from flask_login import login_required, current_user, logout_user

from brewlog import app
from brewlog.config import APP_CONFIG
from brewlog.db_io import record_brew, read_last_brew
from brewlog.login import get_google_auth, get_oath_response, login_oath_user,\
    AUTH_URI


@app.route('/')
@app.route('/index')
@login_required
def index():

    # merge the latest recipe values from the db with the config dict
    latest = read_last_brew()
    if len(latest) != 0:
        recipe = [{**ingredient, 'value': latest[ingredient['name']]}
                  for ingredient in APP_CONFIG['recipe']]
    # if we couldn't load latest values just use the config recipe dict
    else:
        recipe = APP_CONFIG['recipe']

    return render_template('index.html',
                           recipe=recipe,
                           steps=APP_CONFIG['steps'],
                           scores=APP_CONFIG['scores'])


@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    record_brew(request.form)
    return redirect('/')


@app.route('/login')
def login():
    """Login with Google OAuth2."""

    if current_user.is_authenticated:
        return redirect('/')

    google = get_google_auth()

    auth_url, state = google.authorization_url(
        AUTH_URI, access_type='offline')

    return render_template('login.html', auth_url=auth_url)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/gCallback')
def callback():
    """Respond to the Google OAuth2 callback."""

    # Redirect user to home page if already logged in.
    if current_user is not None and current_user.is_authenticated:
        return redirect('/')

    resp = get_oath_response()

    if resp.status_code == 200:
        login_oath_user(resp)
        return redirect('/')

    else:
        return 'Could not fetch your information.'
