import json
import unittest
from jwt import encode
from chapters.methods.post import post, SECRET
from chapters.methods.contrib.db import db


class PostSuite(unittest.TestCase):
    def tearDown(self):
        db.table('user').truncate()
        db.table('post').truncate()
        db.table('chapter').truncate()
        db.table('post_role').truncate()

    def test_post(self):
        user_id = db.table('user').insert_get_id({'name': 'tester'})
        jwt = encode({'user_id': user_id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        db.table('post').insert({'title': 'new post', 'key': 'post_key'})  # noqa: E501
        db.table('post_role').insert({'user_id': user_id, 'post_key': 'post_key', 'type': 'author', 'status': 'active'})  # noqa: E501
        data, meta, message, status_code = post(e={
            'headers': {'Authorization': 'JWT {}'.format(jwt)},
            'body': json.dumps({
                'key': 'chapter_key',
                'post_key': 'post_key',
                'title': 'markdown',
            }),
        })

        self.assertIsNone(message)
        self.assertEqual(meta, None)
        self.assertEqual(status_code, 201)
        self.assertEqual(data['user_id'], user_id)
        self.assertEqual(data['key'], 'chapter_key')
        self.assertEqual(data['post_key'], 'post_key')
