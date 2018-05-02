import unittest
from contrib import db


class ContribSuite(unittest.TestCase):
    def test_db(self):
        result = db.select('select 1 + 1 AS v')

        self.assertEqual(result[0]['v'], 2)
