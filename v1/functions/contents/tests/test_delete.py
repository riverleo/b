import json
import unittest
from jwt import encode
from contents.methods.post import SECRET
from contents.methods.delete import delete
from contents.methods.contrib.db import db


class PostSuite(unittest.TestCase):
    def tearDown(self):
        db.table('user').truncate()
        db.table('post').truncate()
        db.table('page').truncate()
        db.table('content').truncate()
        db.table('post_role').truncate()

    def test_post(self):
        user_id = db.table('user').insert_get_id({'name': 'tester'})
        jwt = encode({'user_id': user_id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        db.table('post').insert_get_id({'title': 'new post', 'key': 'post_key'})  # noqa: E501
        db.table('post_role').insert({'user_id': user_id, 'post_key': 'post_key', 'type': 'author', 'status': 'active'})  # noqa: E501
        db.table('content').insert({'key': 'content_key', 'page_key': 'page_key', 'post_key': 'post_key'})  # noqa: E501
        data, meta, message, status_code = delete(e={
            'headers': {'Authorization': 'JWT {}'.format(jwt)},
            'body': json.dumps({
                'key': 'content_key',
            }),
        })

        content = db.table('content').where('key', 'content_key').first()

        self.assertIsNone(content)
        self.assertIsNone(message)
        self.assertEqual(meta, None)
        self.assertEqual(status_code, 200)
