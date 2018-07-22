import datetime as dt

from collections import ChainMap
from datetime import timedelta
from flask_login import current_user

from brewlog import db
from brewlog.config import APP_CONFIG
from brewlog.models import Brew, ParamRecord, StepRecord, ScoreRecord


def _get_latest_brew_id(cursor):
    """Get the brew_id of the most recent brew."""

    current_id = current_user.user_id

    select_sql = f"SELECT MAX(brew_id) FROM brews WHERE user_id = {current_id}"
    cursor.execute(select_sql)
    brew_id = cursor.fetchone()[0]

    return brew_id


def record_brew(form_dict):
    """Record a brew in the database."""

    # record the timestamp and generate a new brew_id
    brew = Brew(datetime=dt.datetime.now(), user_id=current_user.user_id)
    # flush the session so the brew.brew_id attribute gets populated
    db.session.add(brew)
    db.session.flush()

    # insert the recipe parameter values
    for param in APP_CONFIG['recipe']:
        record = ParamRecord(brew_id=brew.brew_id,
                             param_type=param['name'],
                             value=form_dict[param['name']])
        db.session.add(record)

    # insert the step values along with their odering
    for idx, step in enumerate(APP_CONFIG['steps']):

        # convert strings like '00:01:03' to timedeltas
        mins, secs, h_secs = map(int, form_dict[step['name']].split(':'))
        value = timedelta(minutes=mins, seconds=secs, milliseconds=10*h_secs)

        record = StepRecord(brew_id=brew.brew_id,
                            step_type=step['name'],
                            step_order=idx,
                            value=value)
        db.session.add(record)

    # insert the score values
    for score in APP_CONFIG['scores']:
        record = ScoreRecord(brew_id=brew.brew_id,
                             score_type=score['name'],
                             value=form_dict[score['name']])
        db.session.add(record)

    db.session.commit()


def read_last_brew():
    """Read the parameters of the previous brew."""

    # find the current user's brew with the highest brew_id
    latest_brew = (Brew.query.filter_by(user_id=current_user.user_id)
                             .order_by('-brew_id')
                             .first())

    # return an empty dict if user has no brews
    if latest_brew is None:
        return {}

    # convert each ParamRecord object to a dict, then merge the dicts
    param_dicts = [p.as_dict() for p in latest_brew.params]
    params = dict(ChainMap(*param_dicts))

    return params
