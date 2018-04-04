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
        set_props(new_id(), props={'name': 'riverleo'}, unique=True)

        event = {'body': json.dumps({'props': {'name': 'riverleo'}})}
        res = handler(event, None)

        body = json.loads(res['body'])

        self.assertEqual(res['statusCode'], 200)
        self.assertTrue(body['data']['name']['exists'])
        self.assertEqual(body['data']['name']['value'], 'riverleo')

    def test_not_exists(self):
        event = {'body': json.dumps({'props': {'name': 'riverleo'}})}
        res = handler(event, None)

        body = json.loads(res['body'])

        self.assertEqual(res['statusCode'], 200)
        self.assertFalse(body['data']['name']['exists'])
        self.assertEqual(body['data']['name']['value'], 'riverleo')
