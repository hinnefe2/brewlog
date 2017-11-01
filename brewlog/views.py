from flask import render_template, request, redirect

from brewlog import app
from brewlog.db_io import record_brew, read_last_brew

recipe = [
        {'name': 'wait_cool', 'descr': 'water cool'},
        {'name': 'pour', 'descr': 'pour'},
        {'name': 'wait_bloom', 'descr': 'wait'},
        {'name': 'stir', 'descr': 'stir'},
        {'name': 'wait_stir', 'descr': 'wait'},
        {'name': 'press', 'descr': 'press'}]

@app.route('/')
@app.route('/index')
def index():
    # TODO: read last recipe, autopopulate
    params = read_last_brew()
    return render_template('index.html', steps=recipe, params=params)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    record_brew(request.form)
    return redirect('/')
