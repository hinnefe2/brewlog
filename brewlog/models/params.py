from sqlalchemy import ForeignKey

from brewlog import db


class ParamRecord(db.Model):
    __tablename__ = 'params'
    id = db.Column(db.Integer, primary_key=True)
    brew_id = db.Column(db.Integer, ForeignKey('brews.brew_id'))
    param_type = db.Column(db.String(20), nullable=False)
    value = db.Column(db.String(20), nullable=False)
