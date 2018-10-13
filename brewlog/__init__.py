import os

import matplotlib

from flask import Flask, render_template
from flask_login import LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy

from dash import Dash


app = Flask(__name__)

# need to set the mpl backend before we use pyplot anywhere
# see https://stackoverflow.com/questions/2801882/generating-a-png-with-matplotlib-when-display-is-undefined  # noqa
matplotlib.use('Agg')


class MyDash(Dash):

    def interpolate_index(self, metas='', title='', css='', config='',
                          scripts='', app_entry='', favicon=''):
        return render_template('flask_app.html', scripts=scripts,
                               config=config, app_entry=app_entry)

    def add_url(self, name, view_func, methods=('GET',)):
        self.server.add_url_rule(
            name,
            view_func=login_required(view_func),
            endpoint=name,
            methods=list(methods)
        )


dash_app = MyDash(server=app, url_base_pathname='/analyze/')

# allow non-https oauth callback
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app.config["SECRET_KEY"] = os.getenv("BREWLOG_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("HEROKU_POSTGRESQL_GOLD_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# create the sqlalchemy database object
db = SQLAlchemy(app)

# this module sets up the dash layout and callbacks
from brewlog import analyze  # noqa

from brewlog import views  # noqa
from brewlog.models import User  # noqa

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = None


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(user_id=int(user_id)).first()
