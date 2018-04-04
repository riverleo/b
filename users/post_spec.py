import json
import unittest
from contrib import db
from post import handler


class GetSuite(unittest.TestCase):
    def setUp(self):
        db.table('user').truncate()
        db.table('userProperty').truncate()

    def tearDown(self):
        db.table('user').truncate()
        db.table('userProperty').truncate()

    def test_post(self):
        res = handler({
            'body': json.dumps({
                'props': {
                    'name': 'riverleo',
                    'password': 'wslo1234',
                },
            }),
        }, None)

        body = json.loads(res['body'])

        self.assertIsNotNone(body['data']['id'])
        self.assertEqual(body['data']['props']['name'], 'riverleo')
        self.assertFalse('password' in body['data']['props'])
