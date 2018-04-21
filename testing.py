""" Testing Module """

import unittest as UT
from flask import Flask
from os import remove

import server
from dbmodel import db, Event, seed_db_from_csv

class TestEventClass(UT.TestCase):
    """ Test Event class in dbmodel.py. Uses test database.

        If these tests pass, 'update_param_limits' should also pass, but we
        should confirm the globals are updated in integration testing.

    """

    def setUp(self):
        """ Set up test database and app. """

        # Make app
        test_app = Flask(__name__)

        # Connect app to db
        test_app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///checkrfemaTEST"
        test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.app = test_app
        db.init_app(test_app)

        # Create tables and add test data
        db.create_all()
        # It would be better to unit test these functions before using here, but for
        # space, time, scope, etc. this is fine.
        _create_test_csv()
        seed_db_from_csv('test-data.csv')
        # Remove test data csv file
        remove('test-data.csv')


    def tearDown(self):
        """ Drop data and schema from test db. """

        db.session.close()
        db.drop_all()


    def test_get_earliest_date(self):

        self.assertEqual(Event.get_earliest_date(), '1842-08-25')


    def test_get_latest_date(self):

        self.assertEqual(Event.get_latest_date(), '1875-08-25')


    def test_get_incident_kinds(self):

        self.assertEqual(Event.get_incident_kinds(), ['Earthquake',
                                                      'Flood',
                                                      'Tornado'])

    def test_get_matching_events(self):
        """ Ideally this would test that the filters don't cancel each other out
            and edge cases, but I'm well past a 4-hr time limit.

        """

        start_events = Event.get_matching_events(start_date='1875-01-01')
        end_events = Event.get_matching_events(end_date='1843-01-01')
        kind_events = Event.get_matching_events(kind='Earthquake')
        self.assertEqual(start_events, [Event.query.get(1)])
        self.assertEqual(end_events, [Event.query.get(2)])
        self.assertEqual(kind_events, [Event.query.get(3)])


class TestServerHelperFunctions(UT.TestCase):
    """ Test helper functions in server.py. Does not use db; requires model. """

    def setUp(self):

        server.date_min = "1995-11-15"
        server.date_max = "1995-11-25"


    def test_validate_date(self):

        # Valid dates return unchanged
        self.assertEqual(server.validate_date('1995-11-23'), '1995-11-23')

        # Invalid dates return None
        self.assertIsNone(server.validate_date('1995-11-235'))
        self.assertIsNone(server.validate_date('1995-95-67'))
        self.assertIsNone(server.validate_date('fakedate'))


    def test_unpack_events(self):

        events = [Event('Aliens', '1947-07-08', 'NM', 'Roswell Arrival')]
        unpacked = {0: {'kind': 'Aliens',
                        'date': '1947-07-08',
                        'state': 'NM',
                        'title': 'Roswell Arrival'}}

        self.assertEqual(server.unpack_events(events), unpacked)


##### Test Data #####
def _create_test_csv():
    """ Creates data in test CSV file. """

    events = [['Tornado', '1875-08-25', 'OK', 'OK Tornado'],
              ['Flood', '1842-08-25', 'MI', 'MI Flood'],
              ['Earthquake', '1857-01-18', 'PA', 'PA Earthquake']]

    # Make temporary file and write to it;
    # example from https://stackoverflow.com/a/39110
    with open('test-data.csv', 'w') as test_csv:
        test_csv.write("HEADER ROW\n")
        for event in events:
            # LATER: refactor this to be cleaner and less hard-coded
            test_csv.write(",,,,," +
                           event[2] + "," +
                           event[1] + "," +
                           ",," +
                           event[0] + "," +
                           event[3] + "," +
                           "\n")

    return None


################################################################################

if __name__ == '__main__':
    UT.main()

