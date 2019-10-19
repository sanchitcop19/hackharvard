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

@app.route('/lender/<name>')
def get_lender(name):
    response = jsonify({'data': store['lenders'][name]})
    return response

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
        # TODO: calculate credit score

        credit_score = 0
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
        return render_template('forms/score.html')
    return render_template('forms/register_lendee.html', form=form, submitted = False)

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
