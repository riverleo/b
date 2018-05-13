import json
import unittest
from get_with_id import handler
from props import set_props
from contrib import db, new_id


class GetWithIdSuite(unittest.TestCase):
    def setUp(self):
        db.table('user').truncate()
        db.table('userRole').truncate()
        db.table('userProperty').truncate()

    def tearDown(self):
        db.table('user').truncate()
        db.table('userRole').truncate()
        db.table('userProperty').truncate()

    def test_get_with_id(self):
        user_id = new_id()
        db.table('user').insert(id=user_id)
        set_props(user_id, props={'key': 'value'})

        res = handler({
            'pathParameters': {'id': user_id},
            'queryStringParameters': {'props': 'key,anonymous'},
        }, None)

        body = json.loads(res['body'])

        self.assertEqual(res['statusCode'], 200)
        self.assertEqual(body['data']['id'], user_id)
        self.assertEqual(body['data']['roles'], [])
        self.assertEqual(body['data']['props']['key'], 'value')
        self.assertIsNone(body['data']['props']['anonymous'])
