import json
import unittest
from exists import handler
from props import set_props
from contrib import db, new_id


class GetSuite(unittest.TestCase):
    def setUp(self):
        db.table('user').truncate()
        db.table('userProperty').truncate()

    def tearDown(self):
        db.table('user').truncate()
        db.table('userProperty').truncate()

    def test_exists(self):
        set_props(new_id(), props={'username': 'riverleo'}, unique=True)

        event = {'body': json.dumps({'props': {'username': 'riverleo'}})}
        res = handler(event, None)

        body = json.loads(res['body'])

        self.assertEqual(res['statusCode'], 200)
        self.assertTrue(body['data']['username']['exists'])
        self.assertEqual(body['data']['username']['value'], 'riverleo')

    def test_not_exists(self):
        event = {'body': json.dumps({'props': {'username': 'riverleo'}})}
        res = handler(event, None)

        body = json.loads(res['body'])

        self.assertEqual(res['statusCode'], 200)
        self.assertFalse(body['data']['username']['exists'])
        self.assertEqual(body['data']['username']['value'], 'riverleo')
