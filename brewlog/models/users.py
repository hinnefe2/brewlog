from flask_login.mixins import UserMixin

from brewlog import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=True)

    def get_id(self):
        # NOTE: must return unicode, so str here is python3 specific
        return str(self.user_id)
