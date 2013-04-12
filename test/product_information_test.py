from test.test_base import TestBase
import re

class ProductInfoTest(TestBase):
    def test_product_info(self):
        self.api.get_product_info()

    def test_version(self):
        version = self.api.get_product_info().get_version()
        self.assertTrue(re.match(r'\d',str(version.get_major())), "major version could not be obtained")
        self.assertTrue(re.match(r'\d',str(version.get_minor())), "major version could not be obtained")
        self.assertTrue(re.match(r'\d',str(version.get_build())), "major version could not be obtained")
        self.assertTrue(re.match(r'\d',str(version.get_revision())), "major version could not be obtained")
