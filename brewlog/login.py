import os

from flask_login.mixins import UserMixin
from requests_oauthlib import OAuth2Session


CLIENT_ID = "708447731611-rtlh8cgdutkt1mnjp5psug6uiu8npfg6.apps.googleusercontent.com"  # noqa
REDIRECT_URI = "http://localhost:5000/gCallback"
AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
SCOPE = "https://www.googleapis.com/auth/userinfo.email"
CLIENT_SECRET = os.getenv("BREWLOG_SECRET_KEY")


class User(UserMixin):
    """Class to hold user information for flask-login"""

    def __init__(self, id_):
        self.id = id_


def get_google_auth():
    """Return an OAuth2Session for our Google OAuth setup."""

    return OAuth2Session(CLIENT_ID, scope=SCOPE, redirect_uri=REDIRECT_URI)
