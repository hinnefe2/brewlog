import os

from flask import request
from flask_login import login_user
from requests_oauthlib import OAuth2Session

from brewlog import db
from brewlog.models import User


CLIENT_ID = "708447731611-rtlh8cgdutkt1mnjp5psug6uiu8npfg6.apps.googleusercontent.com"  # noqa
REDIRECT_URI = "https://aerobrewlog.herokuapp.com/gCallback"
REDIRECT_URI_DEV = "http://localhost:5000/gCallback"
AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
SCOPE = ["https://www.googleapis.com/auth/userinfo.email",
         "https://www.googleapis.com/auth/plus.me"]

CLIENT_SECRET = os.getenv("BREWLOG_SECRET_KEY")


def get_google_auth():
    """Return an OAuth2Session for our Google OAuth setup."""

    return OAuth2Session(CLIENT_ID, scope=SCOPE, redirect_uri=REDIRECT_URI_DEV)


def get_oath_response():
    """Return the response of an OAuth request."""

    google = get_google_auth()

    google.fetch_token(TOKEN_URI, client_secret=CLIENT_SECRET,
                       authorization_response=request.url)

    resp = google.get('https://www.googleapis.com/userinfo/v2/me')

    return resp


def login_oath_user(resp):
    """Login a user based on an OAuth request response."""

    resp_data = resp.json()

    # create the user if we don't recognize it
    if User.query.filter_by(email=resp_data['email']).first() is None:

        user = User(email=resp_data['email'], name=resp_data['given_name'])
        db.session.add(user)
        db.session.commit()

    # get the user from the db by email address
    user = User.query.filter_by(email=resp_data['email']).first()

    login_user(user)
