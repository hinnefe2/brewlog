from collections import ChainMap

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

    def as_dict(self):
        param_dicts = [param.as_dict() for param in self.params]
        step_dicts = [step.as_dict() for step in self.steps]
        score_dicts = [score.as_dict() for score in self.scores]

        return dict(ChainMap(*param_dicts, *step_dicts, *score_dicts))
