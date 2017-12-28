import json
import unittest
from jwt import encode
from posts.methods.post import post, SECRET
from posts.methods.contrib.db import db
from posts.methods.contrib.utils import create_random_key


class PostSuite(unittest.TestCase):
    def setUp(self):
        user_id = db.table('user').insert_get_id({'name': 'tester'})
        jwt = (
            encode({'user_id': user_id}, SECRET, algorithm='HS256')
            .decode('utf-8')
        )
        self.event = {'headers': {'Authorization': 'JWT {}'.format(jwt)}}

    def tearDown(self):
        db.table('user').truncate()
        db.table('post').truncate()
        db.table('post_role').truncate()

    def test_invalid_jwt(self):
        _, _, message, status_code = post({'headers': {'Authorization': 'JWT invalid'}})  # noqa: E501

        self.assertEqual(message, 'invalid auth token')
        self.assertEqual(status_code, 401)

    def test_exceed_title_180_characters(self):
        title = create_random_key(length=181)
        self.event['body'] = json.dumps({'title': title})

        _, _, message, status_code = post(self.event)

        self.assertEqual(message, 'title is exceeds 180 characters')
        self.assertEqual(status_code, 403)

    def test_exceed_key_10_characters(self):
        key = create_random_key(length=11)
        self.event['body'] = json.dumps({'key': key})

        _, _, message, status_code = post(self.event)

        self.assertEqual(message, 'key is not string or exceeds 10 characters')
        self.assertEqual(status_code, 403)

    def test_missing_key(self):
        data, _, _, status_code = post(self.event)

        self.assertIsNotNone(data['key'])
        self.assertIsNone(data['title'])
        self.assertIsNone(data['slug'])
        self.assertEqual(status_code, 201)

    def test_dont_modify_slug_if_exists(self):
        self.event['body'] = json.dumps({'key': 'key', 'title': 'new post title'})  # noqa: E501
        data, _, _, status_code = post(self.event)

        self.assertEqual(data['title'], 'new post title')
        self.assertTrue(data['slug'].startswith('new-post-title'))

        self.event['body'] = json.dumps({'key': 'key', 'title': 'change new title'})  # noqa: E501
        data, _, _, status_code = post(self.event)

        self.assertEqual(data['title'], 'change new title')
        self.assertTrue(data['slug'].startswith('new-post-title'))
        self.assertEqual(status_code, 201)

    def test_post(self):
        self.event['body'] = json.dumps({'key': 'valid key', 'title': 'new post title'})  # noqa: E501
        data, _, _, status_code = post(self.event)

        self.assertEqual(data['key'], 'valid key')
        self.assertEqual(data['title'], 'new post title')
        self.assertTrue(data['slug'].startswith('new-post-title'))
        self.assertEqual(status_code, 201)

        self.event['body'] = json.dumps({'key': 'valid key', 'title': ''})  # noqa: E501
        data, _, _, status_code = post(self.event)

        self.assertEqual(db.table('post').count(), 1)
        self.assertEqual(db.table('post_role').count(), 1)
