import json
import unittest
from contrib import db, jwt_encode, new_id
from put import handler


class GetSuite(unittest.TestCase):
    def setUp(self):
        db.table('user').truncate()
        db.table('userProperty').truncate()

    def tearDown(self):
        db.table('user').truncate()
        db.table('userProperty').truncate()

    def test_put(self):
        user_id = new_id()
        db.table('user').insert(id=user_id)

        res = handler({
            'headers': {
                'Authorization': jwt_encode(user_id),
            },
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

    def test_put_nonexistant(self):
        res = handler({
            'headers': {
                'Authorization': jwt_encode(new_id()),
            },
            'body': json.dumps({
                'props': {
                    'name': 'riverleo',
                    'password': 'wslo1234',
                },
            }),
        }, None)

        body = json.loads(res['body'])

        self.assertIsNotNone(body['error'])
