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


@app.route('/api', methods=['GET'])
def return_selected_data():
    """ Returns JSON-formatted data. """

    start = request.args.get('start_date')
    end = request.args.get('end_date')
    kind = request.args.get('event_type')

    events = Event.get_matching_events(start, end, kind)
    return jsonify(code=200, num=len(events), events=unpack_events(events))


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
    print("\nSeeding database.")
    if seed_db_from_csv('fema.csv'):
        print("Database successfully seeded.")
        date_min = Event.get_earliest_date()
        date_max = Event.get_latest_date()
        app.run(port=5000, host='0.0.0.0')
    else:
        print("Database not seeded. Exiting.")