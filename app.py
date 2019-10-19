#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from model import *

DONATION_AMOUNT = 2

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
CORS(app)
app.config.from_object('config')

store = {
    "lenders":
        {
            "sanchit": {
                "total": 0,
                "invested": 0,
                "left": 0,
                "risk_tolerance": 0
            },
            "vignesh": {
                "total": 0,
                "invested": 0,
                "left": 0,
                "risk_tolerance": 0
            }
        },
    "lendees":
        {
            "yuval": {
                "goal": 0,
                "done": 0,
                "credit_score": 0,
                "lenders": [

                ]
            },
            "nien": {
                "goal": 0,
                "done": 0,
                "credit_score": 0,
                "lenders": [

                ]
            }
        }
}

with open("store.json") as f:
    import json
    store = json.load(f)
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return redirect(url_for('register_lendee'))

@app.route('/credit-score')
def credit_score():
    return jsonify({'score': 600})

def invest(lender, lendee, amount):
    if lender in store['lendees'][lendee]['lenders']:
        return
    lender_data = store['lenders'][lender]
    store['lenders'][lender]['invested'] += amount
    store['lenders'][lender]['total'] -= amount
    store['lendees'][lendee]['done'] += amount
    store['lendees'][lendee]['goal'] -= amount
    store['lendees'][lendee]['lenders'].append(lender)

@app.route('/lender/<name>', methods = ["GET", "POST"])
def get_lender(name):
    lender_data = store['lenders'][name]
    form = InvestForm()
    amount = 2
    if form.validate_on_submit():
        for lendee in store['lendees']:
            invest(name, lendee, amount)
    return render_template('forms/lender.html', name = name, total = lender_data['total'], invested = lender_data['invested'], form = form)

@app.route('/lendee/<name>')
def get_lendee(name):
    response = jsonify({'data': store['lendees'][name]})
    return response

@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register_lendee', methods = ["GET", "POST"])
def register_lendee():
    form = RegisterLendeeForm(request.form)
    if form.validate_on_submit():
        confidence, credit_score = compute_credit_confidence(train_model(), [int(form.age.data), int(form.job.data), int(form.credit_amount.data), int(form.duration.data), int(form.sex.data), int(form.housing_own.data), int(form.housing_rent.data), int(form.savings_moderate.data), int(form.savings_quite_rich.data), int(form.savings_rich.data), int(form.check_moderate.data), int(form.check_rich.data)])
        confidence = 80
        credit_score = 750
        store['lendees'][form.name.data] = {
            "goal": int(form.goal.data),
            "done": 0,
            "credit_score": credit_score,
            "lenders": [],
            "origin": form.country_from.data,
            "destination": form.country_to.data
        }
        with open("store.json", "w") as f:
            import json
            json.dump(store, f, indent=4)
        return render_template('forms/score.html', credit_score = credit_score, confidence = confidence)
    return render_template('forms/register_lendee2.html', form=form, submitted = False)

@app.route('/request-investment/<name>')
def request_investment(name):
    lendee = store['lendees'][name]
    for lender in store['lenders']:

        if store['lenders'][lender]['total'] - store['lenders'][lender]['invested'] > 0:
            investment = store['lenders'][lender]['amount']
            store['lenders'][lender]['invested'] += investment
            store['lendees'][name]['done'] += investment
            store['lendees'][name]['lenders'].append(lender)
            if store['lendees'][name]['done'] == store['lendees'][name]['goal']:
                break
    response = jsonify({'data': store['lendees'][name]})
    return response



@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
