import unittest2 as unittest
from factories.api_factory import ApiFactory

class TestBase(unittest.TestCase):
    def setUp(self):
        self.api        = ApiFactory().get_api()

    def tearDown(self):
        self.api.disconnect()
