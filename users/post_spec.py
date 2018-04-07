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
                    'username': 'riverleo',
                    'password': 'wslo1234',
                },
            }),
        }, None)

        body = json.loads(res['body'])

        self.assertIsNotNone(body['data']['id'])
        self.assertIsNotNone(body['data']['ssid'])
        self.assertEqual(body['data']['props']['username'], 'riverleo')
        self.assertFalse('password' in body['data']['props'])
