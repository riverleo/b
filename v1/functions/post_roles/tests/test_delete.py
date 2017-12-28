import json
import unittest
from jwt import encode
from post_roles.methods.delete import delete
from post_roles.methods.post import SECRET
from post_roles.methods.contrib.db import db


class DeleteSuite(unittest.TestCase):
    def tearDown(self):
        db.table('user').truncate()
        db.table('post').truncate()
        db.table('user_role').truncate()
        db.table('post_role').truncate()

    def test_invalid_jwt(self):
        _, _, message, status_code = delete({'headers': {'Authorization': 'JWT invalid'}})  # noqa: E501

        self.assertEqual(message, 'invalid auth token')
        self.assertEqual(status_code, 401)

    def test_no_permission(self):
        user_id = db.table('user').insert_get_id({'name': 'tester'})
        jwt = encode({'user_id': user_id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        _, _, message, status_code = delete({
            'headers': {'Authorization': 'JWT {}'.format(jwt)},
            'body': json.dumps({
                'type': 'author',
                'user_id': -1,
                'post_id': 3,
            }),
        })

        self.assertEqual(message, 'no permission')
        self.assertEqual(status_code, 401)

    def test_invalid_type(self):
        user_id = db.table('user').insert_get_id({'name': 'tester'})
        jwt = encode({'user_id': user_id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        _, _, message, status_code = delete({
            'headers': {'Authorization': 'JWT {}'.format(jwt)},
            'body': json.dumps({
                'type': 'invalid type',
                'user_id': user_id,
                'post_id': 3,
            }),
        })

        self.assertEqual(message, 'params is invalid or the value is empty')
        self.assertEqual(status_code, 403)

    def test_delete(self):
        user_id = db.table('user').insert_get_id({'name': 'tester'})
        jwt = encode({'user_id': user_id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        db.table('post_role').insert_get_id({'type': 'author', 'user_id': user_id, 'post_key': 'post_key'})  # noqa: E501
        db.table('post_role').insert_get_id({'type': 'assistant', 'user_id': user_id, 'post_key': 'post_key'})  # noqa: E501
        _, _, message, status_code = delete({
            'headers': {'Authorization': 'JWT {}'.format(jwt)},
            'body': json.dumps({
                'type': 'author',
                'user_id': user_id,
                'post_key': 'post_key',
            }),
        })

        self.assertIsNone(message)
        self.assertEqual(status_code, 200)

        role_author = db.table('post_role').where('user_id', user_id).where('type', 'author').first()
        role_assistant = db.table('post_role').where('user_id', user_id).where('type', 'assistant').first()

        self.assertIsNone(role_author)
        self.assertIsNotNone(role_assistant)
