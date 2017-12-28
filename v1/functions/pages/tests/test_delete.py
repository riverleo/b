import json
import unittest
from jwt import encode
from pages.methods.post import SECRET
from pages.methods.delete import delete
from pages.methods.contrib.db import db


class PostSuite(unittest.TestCase):
    def tearDown(self):
        db.table('user').truncate()
        db.table('post').truncate()
        db.table('page').truncate()
        db.table('chapter').truncate()
        db.table('post_role').truncate()

    def test_post(self):
        user_id = db.table('user').insert_get_id({'name': 'tester'})
        jwt = encode({'user_id': user_id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        post_id = db.table('post').insert_get_id({'title': 'new post', 'key': 'post_key'})  # noqa: E501
        db.table('post_role').insert({'user_id': user_id, 'post_key': 'post_key', 'type': 'author', 'status': 'active'})  # noqa: E501
        db.table('chapter').insert({'title': 'new chapter', 'key': 'chapter_key', 'post_key': 'post_key'})  # noqa: E501
        db.table('page').insert({'key': 'page_key', 'chapter_key': 'chapter_key', 'post_key': 'post_key'})  # noqa: E501
        data, meta, message, status_code = delete(e={
            'headers': {'Authorization': 'JWT {}'.format(jwt)},
            'body': json.dumps({
                'key': 'page_key',
            }),
        })

        page = db.table('page').where('key', 'page_key').first()

        self.assertIsNone(page)
        self.assertIsNone(message)
        self.assertEqual(meta, None)
        self.assertEqual(status_code, 200)
