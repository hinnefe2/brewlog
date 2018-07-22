from sqlalchemy import ForeignKey

from brewlog import db


class StepRecord(db.Model):
    __tablename__ = 'steps'
    id = db.Column(db.Integer, primary_key=True)
    brew_id = db.Column(db.Integer, ForeignKey('brews.brew_id'))
    step_type = db.Column(db.String(20), nullable=False)
    step_order = db.Column(db.Integer, nullable=False)
    value = db.Column(db.String(20), nullable=False)
