import datetime as dt
import pandas as pd

from collections import ChainMap
from datetime import timedelta
from flask_login import current_user

from brewlog import app, db
from brewlog.config import APP_CONFIG
from brewlog.models import Brew, ParamRecord, StepRecord, ScoreRecord


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


def read_last_recipe():
    """Read the parameters of the previous brew."""

    # find the current user's brew with the highest brew_id
    latest_brew = (Brew.query.filter_by(user_id=current_user.user_id)
                             .order_by(Brew.brew_id.desc())
                             .first())

    # return the recipe without any values filled in if user doesn't hve any
    # previous brews
    if latest_brew is None:
        return APP_CONFIG['recipe']

    # convert each ParamRecord object to a dict, then merge the dicts
    param_dicts = [p.as_dict() for p in latest_brew.params]
    values = dict(ChainMap(*param_dicts))

    # merge the latest recipe values from the db with the config dict
    recipe = [{**ingredient, 'value': values[ingredient['name']]}
              for ingredient in APP_CONFIG['recipe']]

    return recipe


def load_wide_table():

    app.logger.info('trying to load wide table')

    if not current_user:
        app.logger.info('no current_user')
        return pd.DataFrame()

    app.logger.info('loading user brews')
    user_brews = Brew.query.filter_by(user_id=current_user.user_id)
    brews = (pd.read_sql(user_brews.statement, db.session.bind)
               .set_index('brew_id'))

    # return an empty dataframe if the user doesn't have any brews recorded
    if len(brews) == 0:
        return pd.DataFrame()

    # load each table all at once
    steps = pd.read_sql(StepRecord.query.statement, db.session.bind)
    params = pd.read_sql(ParamRecord.query.statement, db.session.bind)
    scores = pd.read_sql(ScoreRecord.query.statement, db.session.bind)

    # pivot the long-form tables from the db into wide-form dataframes
    params_wide = params.pivot(index='brew_id', columns='param_type', values='value')
    scores_wide = scores.pivot(index='brew_id', columns='score_type', values='value')
    steps_wide = steps.pivot(index='brew_id', columns='step_type', values='value')

    # join the pivoted tables and drop some obsolete columns
    app.logger.info('making dataframe')
    wide = (brews.join(steps_wide)
                 .join(params_wide)
                 .join(scores_wide)
                 .drop(['done', 'amount'], axis='columns'))

    # convert numeric columns to floats
    for col in ['coffee', 'grind', 'temp', 'water']:
        wide[col] = wide[col].apply(float)

    # convert timedeltas to total_seconds bc json-serializing them is a pain
    for col in wide.select_dtypes('timedelta'):
        wide[col] = wide[col].apply(lambda r: r.total_seconds())

    return wide


def calculate_features(wide):
    """Calculate derived feature values."""

    wide['immersion_time'] = (wide.press - wide.wait_cool)
    wide['ratio'] = wide.water / wide.coffee
    wide['composite_score'] = wide.overall - 0.1 * wide.sour - 0.1 * wide.bitter
    wide['water_cooldown'] = wide.wait_cool

    return wide
