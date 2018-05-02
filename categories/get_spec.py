import json
import unittest
from contrib import db
from get import handler


class GetSuite(unittest.TestCase):
    def setUp(self):
        db.table('category').truncate()

    def tearDown(self):
        db.table('category').truncate()

    def test_get(self):
        db.table('category').insert(key='category1')
        db.table('category').insert(key='category2')
        db.table('category').insert(key='category3')

        res = handler(None, None)
        body = json.loads(res['body'])

        self.assertIsNotNone(body['data'])
        self.assertEqual(len(body['data']), 3)
