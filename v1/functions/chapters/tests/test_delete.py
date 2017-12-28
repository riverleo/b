import json
import unittest
from jwt import encode
from chapters.methods.post import SECRET
from chapters.methods.delete import delete
from chapters.methods.contrib.db import db


class PostSuite(unittest.TestCase):
    def tearDown(self):
        db.table('user').truncate()
        db.table('post').truncate()
        db.table('chapter').truncate()
        db.table('post_role').truncate()

    def test_delete(self):
        user_id = db.table('user').insert_get_id({'name': 'tester'})
        jwt = encode({'user_id': user_id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        post_id = db.table('post').insert_get_id({'title': 'new post', 'key': 'post_key'})  # noqa: E501
        db.table('post_role').insert({'user_id': user_id, 'post_key': 'post_key', 'type': 'author', 'status': 'active'})  # noqa: E501
        db.table('chapter').insert({'title': 'new chapter', 'key': 'chapter_key', 'post_key': 'post_key'})  # noqa: E501
        data, meta, message, status_code = delete(e={
            'headers': {'Authorization': 'JWT {}'.format(jwt)},
            'body': json.dumps({
                'key': 'chapter_key',
            }),
        })

        chapter = db.table('chapter').where('key', 'chapter_key').first()

        self.assertIsNone(chapter)
        self.assertIsNone(message)
        self.assertEqual(meta, None)
        self.assertEqual(status_code, 200)

    def test_delete_by_key(self):
        user_id = db.table('user').insert_get_id({'name': 'tester'})
        jwt = encode({'user_id': user_id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        post_id = db.table('post').insert_get_id({'title': 'new post', 'key': 'post_key'})  # noqa: E501
        db.table('post_role').insert({'user_id': user_id, 'post_key': 'post_key', 'type': 'author', 'status': 'active'})  # noqa: E501
        db.table('chapter').insert({'title': 'new chapter', 'key': 'chapter_key', 'post_key': 'post_key'})  # noqa: E501
        data, meta, message, status_code = delete(e={
            'headers': {'Authorization': 'JWT {}'.format(jwt)},
            'pathParameters': {
                'id': 'chapter_key',
            },
        })

        chapter = db.table('chapter').where('key', 'chapter_key').first()

        self.assertIsNone(chapter)
        self.assertIsNone(message)
        self.assertEqual(meta, None)
        self.assertEqual(status_code, 200)

    def test_delete_by_id(self):
        user_id = db.table('user').insert_get_id({'name': 'tester'})
        jwt = encode({'user_id': user_id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        post_id = db.table('post').insert_get_id({'title': 'new post', 'key': 'post_key'})  # noqa: E501
        db.table('post_role').insert({'user_id': user_id, 'post_key': 'post_key', 'type': 'author', 'status': 'active'})  # noqa: E501
        chapter_id = db.table('chapter').insert_get_id({'title': 'new chapter', 'key': 'chapter_key', 'post_key': 'post_key'})  # noqa: E501
        data, meta, message, status_code = delete(e={
            'headers': {'Authorization': 'JWT {}'.format(jwt)},
            'pathParameters': {
                'id': str(chapter_id),
            },
        })

        chapter = db.table('chapter').where('id', chapter_id).first()

        self.assertIsNone(chapter)
        self.assertIsNone(message)
        self.assertEqual(meta, None)
        self.assertEqual(status_code, 200)
