""" DB ORM Flask-SQLAlchemy """

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

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
    title = db.Column(db.Text)

    def __init__(self, kind, date=None, state=None, title=None):
        self.kind = kind
        self.date = date
        self.state = state
        self.title = title

    def __repr__(self):
        return '<Event {:16} {} {} {:.30}>'.format(self.kind,
                                                   self.date,
                                                   self.state,
                                                   self.title)


    @classmethod
    def get_earliest_date(cls):
        """ Return earliest date in database. """

        return cls.query.order_by(cls.date).first().date


    @classmethod
    def get_latest_date(cls):
        """ Return latest date in database. """

        return cls.query.order_by(desc(cls.date)).first().date


    @classmethod
    def get_incident_kinds(cls):
        """ Return list of incident kinds in database. """

        kinds = db.session.query(cls.kind.distinct()).all()
        return sorted([kind[0] for kind in kinds])


    @classmethod
    def get_matching_events(cls, start_date=None, end_date=None, kind=None):
        """ Returns all objects that match a structured query. """

        query = cls.query.order_by(cls.date)

        if start_date:
            query = query.filter(cls.date >= start_date)

        if end_date:
            query = query.filter(cls.date <= end_date)

        if kind and kind != 'all':
            query = query.filter(cls.kind == kind)

        return query.all()


###### HELPER FUNCTIONS #####

def connect_to_db(app):
    """ Connect the database to a Flask app. """

    # Configure to use PostgreSQL database
    # (Move this to environment variables after proof of concept)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///checkrfema"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    # create_all() does not edit existing data, but can update schema
    # ... which might cause some problems if data exists
    db.create_all()


def seed_db_from_csv(csv):
    """ Seed the database from the provided CSV file. It relies heavily on the
        format originally provided.

    """

    # Delete any existing rows
    Event.query.delete()
    db.session.commit()

    with open(csv, 'r') as csv_file:
        # Skip the first row of column headers
        rows = [row.strip().split(',')[:11] for row in csv_file.readlines()[1:]]

    for _, _, _, _, _, state, date, _, _, kind, title in rows:
        event = Event(kind, date=date[:10], state=state, title=title.strip('"'))
        db.session.add(event)

    try:
        # Persist changes if entire table was imported successfully
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False


def update_param_limits():
    """ Update three globals. Ought to be called on database change. """

    date_min = Event.get_earliest_date()
    date_max = Event.get_latest_date()
    kinds = Event.get_incident_kinds()

    return None


################################################################################

if __name__ == '__main__':

    # Start Flask app
    from flask import Flask
    app = Flask(__name__)

    # Connect to DB
    connect_to_db(app)
    print("\n-- Working directly in database. Use Flask-SQLAlchemy syntax. --\n")