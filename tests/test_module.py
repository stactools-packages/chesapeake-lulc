import unittest

import stactools.cclc


class TestModule(unittest.TestCase):

    def test_version(self):
        self.assertIsNotNone(stactools.cclc.__version__)
