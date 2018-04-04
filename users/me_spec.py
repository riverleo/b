import json
import unittest
from me import handler
from props import set_props
from contrib import db, jwt_encode, new_id


class GetSuite(unittest.TestCase):
    def setUp(self):
        db.table('user').truncate()
        db.table('userProperty').truncate()

    def tearDown(self):
        db.table('user').truncate()
        db.table('userProperty').truncate()

    def test_get_props(self):
        user_id = new_id()
        db.table('user').insert(id=user_id)
        set_props(user_id, props={'key': 'value'})
        encoded = jwt_encode(user_id)

        res = handler({
            'body': json.dumps({'props': ['key', 'anonymous']}),
            'headers': {'Authorization': 'Bearer {}'.format(encoded)},
        }, None)

        body = json.loads(res['body'])

        self.assertEqual(res['statusCode'], 200)
        self.assertEqual(body['data']['id'], user_id)
        self.assertEqual(body['data']['props']['key'], 'value')
        self.assertIsNone(body['data']['props']['anonymous'])