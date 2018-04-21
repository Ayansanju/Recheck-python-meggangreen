""" Application """

from dbmodel import *
from flask import Flask, request, jsonify, render_template
from jinja2 import StrictUndefined
import json
from datetime import datetime

# Start Flask app
app = Flask(__name__)

# Make Jinja raise an error if it encounters an undefined variable
app.jinja_env.undefined = StrictUndefined


##### Globals #####
# Param Limits
# These values could change as records are added or modified;
# they ought to be initialized from the get go
date_min = None
date_max = None
kinds = None


##### Routes #####
@app.route('/')
def return_index():
    """ Return index.html. """

    return render_template("index.html", date_min=date_min,
                                         date_max=date_max,
                                         kinds=kinds)


@app.route('/api', methods=['GET'])
def return_selected_data():
    """ Returns JSON-formatted data. """

    # Validate data
    start = validate_date(request.args.get('start'))
    end = validate_date(request.args.get('end'))
    kind = request.args.get('kind') if request.args.get('kind') in kinds else None

    events = Event.get_matching_events(start, end, kind)

    return jsonify(code=200, count=len(events), events=unpack_events(events))


##### Helper Functions #####
def validate_date(date):
    """ Returns the validated date as string or None. """

    # Check if string is a date and in the correct format
    try:
        date_dt = datetime.strptime(date, '%Y-%m-%d')
    except:
        return None

    # Convert min and max to datetime objects
    date_min_dt = datetime.strptime(date_min, '%Y-%m-%d')
    date_max_dt = datetime.strptime(date_max, '%Y-%m-%d')

    # Return date if within parameters
    if date_min_dt <= date_dt <= date_max_dt:
        return date

    return None


def unpack_events(events):
    """ Takes in a list of event objects and returns a dictionary for JSON. """

    events_dict = {}

    for i in range(len(events)):
        events_dict[i] = {'kind': events[i].kind,
                          'date': events[i].date,
                          'state': events[i].state,
                          'title': events[i].title}

    return events_dict


################################################################################
##### Run App #####

if __name__ == '__main__':

    # Connect to DB and seed; run app if successful
    connect_to_db(app)

    # Seeding takes a long time, but if the db is empty, we can't run
    okay_to_run = True if Event.query.first() else seed_db_from_csv('fema.csv')

    # Run the app if everything is okay
    if okay_to_run:
        print("Starting app.")
        update_param_limits()
        app.run(port=5000, host='0.0.0.0')
    else:
        print("Exiting.")