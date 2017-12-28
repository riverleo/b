import unittest
from jwt import encode
from json import loads
from upload.methods.post import post, SECRET
from upload.methods.contrib.db import db


class PostSuite(unittest.TestCase):
    def tearDown(self):
        db.table('user').truncate()
        db.table('file').truncate()

    def test_post(self):
        id = db.table('user').insert_get_id({'name': 'tester'})
        jwt = encode({'user_id': id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        e = {
            'queryStringParameters': {
                'name': 'input.txt',
            },
            'headers': {
                'Content-Type': 'text/plain',
                'Authorization': 'JWT {}'.format(jwt),
            },
            'body': 'input',
        }

        data, meta, message, status_code = post(e)

        self.assertEqual(meta, None)
        self.assertEqual(message, None)
        self.assertEqual(status_code, 201)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['user_id'], 1)
        self.assertIsNone(data['attachable_id'])
        self.assertIsNone(data['attachable_type'])
        self.assertIsNotNone(data['key'])
        self.assertEqual(data['bucket'], 'static.scdc.co')
        self.assertEqual(data['name'], 'input.txt')
        self.assertEqual(data['type'], 'text/plain')
        self.assertEqual(data['size'], 5.0)
