from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from brewlog import db


class Brew(db.Model):
    __tablename__ = 'brews'
    brew_id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('users.user_id'), nullable=True)

    params = relationship('ParamRecord')
    steps = relationship('StepRecord')
    scores = relationship('ScoreRecord')
