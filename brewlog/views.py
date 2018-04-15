from flask import render_template, request, redirect
from flask_login import login_required, login_user, current_user, logout_user

from brewlog import app
from brewlog.db_io import record_brew, read_last_brew
from brewlog.login import get_google_auth, AUTH_URI, TOKEN_URI, \
        CLIENT_SECRET, User


recipe = [
        {'name': 'wait_cool', 'descr': 'water cool'},
        {'name': 'pour', 'descr': 'pour'},
        {'name': 'wait_bloom', 'descr': 'wait'},
        {'name': 'stir', 'descr': 'stir'},
        {'name': 'wait_stir', 'descr': 'wait'},
        {'name': 'press', 'descr': 'press'}]


@app.route('/')
@app.route('/index')
@login_required
def index():
    # TODO: read last recipe, autopopulate
    params = read_last_brew()
    return render_template('index.html', steps=recipe, params=params)


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

    google = get_google_auth()
    google.fetch_token(TOKEN_URI, client_secret=CLIENT_SECRET,
                       authorization_response=request.url)

    resp = google.get('https://www.googleapis.com/userinfo/v2/me')

    if resp.status_code == 200:

        user = User(resp.json()['email'])
        login_user(user)

        return redirect('/')

    else:
        return 'Could not fetch your information.'
