""" Application """

from dbmodel import *
from flask import Flask, request, jsonify, render_template
from jinja2 import StrictUndefined
import json, re

# Start Flask app
app = Flask(__name__)

# Make Jinja raise an error if it encounters an undefined variable
app.jinja_env.undefined = StrictUndefined


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

    if re.search(DATE_PATTERN, date) and ( date_min <= date <= date_max ):
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
        # Constant
        DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        # These values could change as records are added or modified;
        # they ought to be initialized from the get go
        date_min = Event.get_earliest_date()
        date_max = Event.get_latest_date()
        kinds = Event.get_incident_kinds()
        # Run
        app.run(port=5000, host='0.0.0.0')
    else:
        print("Exiting.")