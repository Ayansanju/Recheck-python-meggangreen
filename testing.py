""" Testing Module """

import unittest as UT
import server
# from selenium import webdriver

def setUpModule():
    """ Set up browser and mock up database. """

    server.date_min = "1995-11-15"
    server.date_max = "1995-11-25"
    server.kinds = ["Danger Will Robinson", "We're Losing Shields"]

    # broswer = webdriver.Firefox()


def tearDownModule():
    """ Close down browser. """

    pass
    # browser.quit()


class TestServerHelperFunctions(UT.TestCase):
    """ Test helper functions in server.py """

    def test_validate_date(self):

        # Valid dates return unchanged
        self.assertEqual(server.validate_date('1995-11-23'), '1995-11-23')

        # Invalid dates return None
        self.assertIsNone(server.validate_date('1995-11-235'))
        self.assertIsNone(server.validate_date('5845-95-67'))
        self.assertIsNone(server.validate_date('fakedate'))


################################################################################

if __name__ == '__main__':
    UT.main()

