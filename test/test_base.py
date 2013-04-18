import unittest2 as unittest
from factories.api_factory import ApiFactory
from config.config import Config

class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = ApiFactory().get_api(**Config.get_instance().rest_api)

    @classmethod
    def tearDownClass(cls):
        cls.api.disconnect()
