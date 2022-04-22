import unittest

import stactools.chesapeake_lulc


class TestModule(unittest.TestCase):

    def test_version(self):
        self.assertIsNotNone(stactools.chesapeake_lulc.__version__)
