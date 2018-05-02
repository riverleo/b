import json
import unittest
from contrib import db
from post import handler


class PostSuite(unittest.TestCase):
    def setUp(self):
        db.table('work').truncate()

    def tearDown(self):
        db.table('work').truncate()

    def test_post(self):
        body = json.loads(handler({
            'body': json.dumps({
                'id': 'id',
                'contents': 'contents',
            }),
        }, None)['body'])

        self.assertEqual(body['data']['id'], 'id')
        self.assertEqual(body['data']['contents'], 'contents')
        self.assertIsNotNone(body['data']['createdAt'])
