# flake8: noqa

APP_CONFIG = {
    'recipe': [
        {'name': 'roaster', 'descr': 'Roaster', 'type': 'text'},
        {'name': 'beans', 'descr': 'Beans', 'type': 'text'},
        {'name': 'roast_date', 'descr': 'Roast date (MM/DD/YY)', 'type': 'text'},
        {'name': 'coffee', 'descr': 'Coffee (g)', 'type': 'number'},
        {'name': 'grind', 'descr': 'Grind', 'type': 'number'},
        {'name': 'temp', 'descr': 'Temperature (F)', 'type': 'number'},
        {'name': 'water', 'descr': 'Water (g)', 'type': 'number'}
        ],
    'steps': {
        'aeropress': [
            {'name': 'wait_cool', 'descr': 'water cool'},
            {'name': 'pour', 'descr': 'pour'},
            {'name': 'wait_bloom', 'descr': 'wait'},
            {'name': 'stir', 'descr': 'stir'},
            {'name': 'wait_stir', 'descr': 'wait'},
            {'name': 'press', 'descr': 'press'}
            ],
        'pourover': [
            {'name': 'wait_cool', 'descr': 'water cool'},
            {'name': 'bloom', 'descr': 'bloom'},
            {'name': 'pour', 'descr': 'pour'},
            {'name': 'wait_drip', 'descr': 'wait_drip'},
            ],
        }
    'scores': [
        {'name': 'sour', 'descr': 'Sourness'},
        {'name': 'bitter', 'descr': 'Bitterness'},
        {'name': 'strength', 'descr': 'Strength'},
        {'name': 'smell', 'descr': 'Smell'},
        {'name': 'finish', 'descr': 'Finish'},
        {'name': 'overall', 'descr': 'Overall'}
        ]}
