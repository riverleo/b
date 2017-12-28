import json
import unittest
from create.methods.post import post
from create.methods.contrib.db import db


class PostSuite(unittest.TestCase):
    def tearDown(self):
        db.table('link').truncate()

    def test_invalid_href(self):
        data, meta, message, status_code = post({
            'body': json.dumps({
                'href': '',
            }),
        })

        self.assertEqual(data, None)
        self.assertEqual(meta, None)
        self.assertEqual(message, '`href` is invalid')
        self.assertEqual(status_code, 403)

    def test_post(self):
        data, meta, message, status_code = post({
            'body': json.dumps({
                'href': 'https://wearescdc.com',
            }),
        })

        self.assertIsNotNone(data['id'])
        self.assertIsNotNone(data['key'])
        self.assertEqual(data['href'], 'https://wearescdc.com')
        self.assertEqual(data['link'], 'scdc.co/{}'.format(data['key']))
        self.assertEqual(meta, None)
        self.assertEqual(message, None)
        self.assertEqual(status_code, 201)
