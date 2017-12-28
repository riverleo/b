import json
import unittest
from jwt import encode
from user_roles.methods.delete import delete
from user_roles.methods.post import SECRET
from user_roles.methods.contrib.db import db


class DeleteSuite(unittest.TestCase):
    def tearDown(self):
        db.table('user').truncate()
        db.table('user_role').truncate()

    def test_invalid_jwt(self):
        _, _, message, status_code = delete({'headers': {'Authorization': 'JWT invalid'}})  # noqa: E501

        self.assertEqual(message, 'invalid auth token')
        self.assertEqual(status_code, 401)

    def test_no_permission(self):
        id = db.table('user').insert_get_id({'name': 'tester'})
        jwt = encode({'user_id': id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        _, _, message, status_code = delete({'headers': {'Authorization': 'JWT {}'.format(jwt)}})  # noqa: E501

        self.assertEqual(message, 'no permission')
        self.assertEqual(status_code, 401)

    def test_missing_type_param(self):
        id = db.table('user').insert_get_id({'name': 'tester'})
        jwt = encode({'user_id': id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        _, _, message, status_code = delete({'headers': {'Authorization': 'JWT {}'.format(jwt)}, 'body': json.dumps({'user_id': id})})  # noqa: E501

        self.assertEqual(message, 'type is invalid or the value is empty')
        self.assertEqual(status_code, 403)

    def test_delete_by_deactivated_role(self):
        id = db.table('user').insert_get_id({'name': 'tester'})
        db.table('user_role').insert(user_id=id, type='admin', status='disable')
        jwt = encode({'user_id': id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        _, _, message, status_code = delete({'headers': {'Authorization': 'JWT {}'.format(jwt)}, 'body': json.dumps({'user_id': id})})  # noqa: E501

        self.assertEqual(message, 'type is invalid or the value is empty')
        self.assertEqual(status_code, 403)
        pass

    def test_delete(self):
        id = db.table('user').insert_get_id({'name': 'tester'})
        db.table('user_role').insert(user_id=id, type='admin', status='active')
        db.table('user_role').insert(user_id=id, type='author', status='active')
        jwt = encode({'user_id': id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        _, _, message, status_code = delete({'headers': {'Authorization': 'JWT {}'.format(jwt)}, 'body': json.dumps({'type': 'author', 'user_id': id})})  # noqa: E501

        role_admin = (
            db.table('user_role')
            .where('user_id', id)
            .where('type', 'admin')
            .first()
        )

        role_author = (
            db.table('user_role')
            .where('user_id', id)
            .where('type', 'author')
            .first()
        )

        self.assertEqual(status_code, 200)
        self.assertEqual(role_admin['status'], 'active')
        self.assertIsNone(role_author)
