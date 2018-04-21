""" Testing Module """

import unittest as UT
from selenium import webdriver

def setUpModule():
    """ Set up browser and mock up database. """

    broswer = webdriver.Firefox()


def tearDownModule():
    """ Close down browser. """

    browser.quit()


class TestServerHelperFunctions(UT.TestCase):
    """ Test helper functions in server.py """

    def test_all_functions(self):
        pass
        # self.assertEqual(unittest_results, dataset.results)


################################################################################

if __name__ == '__main__':
    UT.main()

