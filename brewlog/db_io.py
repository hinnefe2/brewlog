import os

import datetime as dt
import psycopg2 as pg2
import psycopg2.sql as sql

from urllib import parse


SCORES = {'table_name': 'scores',
          'type_col': 'score_type',
          'types': ['sour', 'bitter', 'strength', 'smell', 'finish',
                    'overall']}

PARAMS = {'table_name': 'params',
          'type_col': 'param_type',
          'types': ['roaster', 'beans', 'coffee', 'grind', 'temp', 'water']}

TIMES = {'table_name': 'steps',
         'type_col': 'step_type',
         'types': ['wait_cool', 'pour', 'wait_bloom', 'stir', 'wait_stir',
                   'press', 'done']}


def _insert(cursor, brew_id, form_dict, table_name, type_col, types):
    """Insert values into a normalized table in the database."""

    # psycopg2s sql module appears to be a pain in the ass, so we're gonna just
    # use python string formatting, at least for values we control
    insert_sql = ("INSERT INTO {} (brew_id, {}, value) VALUES (%s, %s, %s)"
                  .format(table_name, type_col))

    for typ in types:
        cursor.execute(insert_sql, [brew_id, typ, form_dict[typ]])


def _get_latest_brew_id(cursor):
    """Get the brew_id of the most recent brew."""

    select_sql = "SELECT MAX(brew_id) FROM brews"
    cursor.execute(select_sql)
    brew_id = cursor.fetchone()[0]

    return brew_id


def record_brew(form_dict):
    """Record a brew in the database."""

    parse.uses_netloc.append("postgres")
    url = parse.urlparse(os.environ["DATABASE_URL"])

    with pg2.connect(database=url.path[1:], user=url.username,
                     password=url.password, host=url.hostname, port=url.port) as conn:
        with conn.cursor() as curr:

            # record the timestamp and generate a new brew_id
            insert_sql = sql.SQL("INSERT INTO brews (datetime) VALUES ({});")
            now = sql.Literal(dt.datetime.now().strftime('%Y-%m-%d %H:%M'))
            curr.execute(insert_sql.format(now))

            # get the newly generated brew_id
            brew_id = _get_latest_brew_id(curr)

            # insert the brew parameters
            _insert(curr, brew_id, form_dict, **PARAMS)

            # insert the brew steps
            _insert(curr, brew_id, form_dict, **TIMES)

            # insert the brew scores
            _insert(curr, brew_id, form_dict, **SCORES)


def read_last_brew():
    """Read the parameters of the previous brew."""

    params = {}

    parse.uses_netloc.append("postgres")
    url = parse.urlparse(os.environ["DATABASE_URL"])

    with pg2.connect(database=url.path[1:], user=url.username,
                     password=url.password, host=url.hostname, port=url.port) as conn:
        with conn.cursor() as curr:

            # get the parameters of the most recent brew
            select_sql = "SELECT param_type, value FROM params WHERE brew_id = %s"
            brew_id = _get_latest_brew_id(curr)
            curr.execute(select_sql, [brew_id])

            # populate a dictionary of {param_type: values}
            for row in curr.fetchall():
                param_type, value = row
                params[param_type] = value

    return params
