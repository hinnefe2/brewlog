import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# allow non-https oauth callback
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app.config["SECRET_KEY"] = os.getenv("BREWLOG_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("HEROKU_POSTGRESQL_GOLD_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# create the sqlalchemy database object
db = SQLAlchemy(app)

from brewlog import views  # noqa
from brewlog.models import User  # noqa

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = None


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(user_id=int(user_id)).first()
