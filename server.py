""" Application """

from dbmodel import *
from flask import Flask, request, jsonify, render_template

# Start Flask app
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "checkrfema"

# Make Jinja raise an error if it encounters an undefined variable
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def return_index():
    """ Return index.html. """

    return render_template("index.html", date_min=date_min, date_max=date_max)


################################################################################
##### Run App #####

if __name__ == '__main__':

    # Connect to DB and seed; run app if successful
    connect_to_db(app)
    print("\nSeeding database.")
    if seed_db_from_csv('fema.csv'):
        print("Database successfully seeded.")
        date_min = Event.get_earliest_date()
        date_max = Event.get_latest_date()
        app.run(port=5000, host='0.0.0.0')
    else:
        print("Database not seeded. Exiting.")