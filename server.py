""" Application """

from dbmodel import *
from flask import Flask, request, jsonify


################################################################################
##### Run App #####

if __name__ == '__main__':

    # Start Flask app
    app = Flask(__name__)

    # Connect to DB and seed; run app if successful
    connect_to_db(app)
    print("\nSeeding database.")
    if seed_db_from_csv('fema.csv'):
        print("Database successfully seeded.")
        app.run(port=5000, host='0.0.0.0')
    else:
        print("Database not seeded. Exiting.")