import unittest
from jwt import encode
from posts.methods.contrib.db import db
from posts.methods.post import SECRET
from posts.methods.delete import delete


class DeleteSuite(unittest.TestCase):
    def setUp(self):
        self.user_id = db.table('user').insert_get_id({'name': 'tester'})
        jwt = (
            encode({'user_id': self.user_id}, SECRET, algorithm='HS256')
            .decode('utf-8')
        )
        self.event = {'headers': {'Authorization': 'JWT {}'.format(jwt)}}

    def tearDown(self):
        db.table('user').truncate()
        db.table('post').truncate()
        db.table('post_role').truncate()

    def test_invalid_jwt(self):
        _, _, message, status_code = delete({'headers': {'Authorization': 'JWT invalid'}})  # noqa: E501

        self.assertEqual(message, 'invalid auth token')
        self.assertEqual(status_code, 401)

    def test_no_permission(self):
        id_ = db.table('post').insert_get_id({'title': 'Post'})

        self.event['pathParameters'] = {'id': id_}
        _, _, message, status_code = delete(self.event)

        post = db.table('post').where('id', id_).first()

        self.assertEqual(message, 'no permission')
        self.assertEqual(status_code, 401)
        self.assertIsNotNone(post)

    def test_no_permission_by_deactivated_role(self):
        id_ = db.table('post').insert_get_id({'key': 'key', 'title': 'Post'})
        db.table('post_role').insert({'user_id': self.user_id, 'post_key': 'key', 'status': 'pending'})  # noqa: E501
        db.table('post_role').insert({'user_id': self.user_id, 'post_key': 'key', 'status': 'disable'})  # noqa: E501
        db.table('post_role').insert({'user_id': self.user_id, 'post_key': 'key', 'status': 'request'})  # noqa: E501

        self.event['pathParameters'] = {'id': id_}
        _, _, message, status_code = delete(self.event)

        post = db.table('post').where('id', id_).first()

        self.assertEqual(message, 'no permission')
        self.assertEqual(status_code, 401)
        self.assertIsNotNone(post)

    def test_delete(self):
        id_ = db.table('post').insert_get_id({'key': 'post_key', 'title': 'Post'})
        db.table('post_role').insert({'user_id': self.user_id, 'post_key': 'post_key', 'status': 'active'})  # noqa: E501

        self.event['pathParameters'] = {'id': id_}
        _, _, message, status_code = delete(self.event)

        post = db.table('post').where('id', id_).first()

        self.assertIsNone(message)
        self.assertEqual(status_code, 200)
        self.assertIsNotNone(post['deleted_at'])
