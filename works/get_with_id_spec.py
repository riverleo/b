import unittest
from contrib import db


class GetWithIdSuite(unittest.TestCase):
    def setUp(self):
        db.table('work').truncate()

    def tearDown(self):
        db.table('work').truncate()

    def test_get_with_id(self):
        pass
