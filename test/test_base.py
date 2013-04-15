import unittest2 as unittest
from factories.api_factory import ApiFactory

class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api        = ApiFactory().get_api()

    @classmethod
    def tearDownClass(cls):
        cls.api.disconnect()
