from sqlalchemy import ForeignKey

from brewlog import db


class ScoreRecord(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)
    brew_id = db.Column(db.Integer, ForeignKey('brews.brew_id'))
    score_type = db.Column(db.String(20), nullable=False)
    value = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {self.score_type: self.value}
