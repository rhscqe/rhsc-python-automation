import unittest2 as unittest
from config.config import Config

class ConfigTest(unittest.TestCase):

    def test_config(self):
        json  = Config().to_json()
        config =  Config.from_json(json)
        self.assertEquals(config.rest_api, Config().rest_api)

    def test_get_instance(self):
        Config.get_instance().rest_api
