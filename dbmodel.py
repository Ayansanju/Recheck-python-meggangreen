""" DB ORM Flask-SQLAlchemy """

from flask_sqlalchemy import SQLAlchemy





###### HELPER FUNCTIONS #####

def connect_to_db(app):
    """ Connect the database to a Flask app. """

    # Configure to use PostgreSQL database
    # (Move this to environment variables after proof of concept)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///checkrfema'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    # creat_all() does not edit existing data, but can update schema
    # ... which might cause some problems if data exists
    db.create_all()


################################################################################

if __name__ == '__main__':

    # Start Flask app
    from flask import Flask
    app = Flask(__name__)

    # Connect to DB
    connect_to_db(app)
    print("\n-- Working directly in database. Use Flask-SQLAlchemy syntax. --\n")