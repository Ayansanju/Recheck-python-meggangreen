""" DB ORM Flask-SQLAlchemy """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##### CLASSES #####

class Event(db.Model):
    """ Each record in the FEMA CSV file is an Event. We will track only some
        information for this project.
    """

    __tablename__ = 'events'

    evt_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kind = db.Column(db.Text, nullable=False)  # Incident Type
    date = db.Column(db.String(10), nullable=False)  # Declaration Date
    state = db.Column(db.Text, nullable=False)  # State where disaster occurred

    def __init__(self, kind, date=None, state=None):
        self.kind = kind
        self.date = date
        self.state = state

    def __repr__(self):
    return '<Event {} {} {}>'.format(self.kind, self.date, self.state)


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