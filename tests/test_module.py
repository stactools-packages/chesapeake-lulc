import unittest

import stactools.chesapeake


class TestModule(unittest.TestCase):

    def test_version(self):
        self.assertIsNotNone(stactools.chesapeake.__version__)
