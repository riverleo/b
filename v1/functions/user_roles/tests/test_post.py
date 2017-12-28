import json
import unittest
from jwt import encode
from user_roles.methods.post import post, SECRET
from user_roles.methods.contrib.db import db


class PostSuite(unittest.TestCase):
    def tearDown(self):
        db.table('user').truncate()
        db.table('user_role').truncate()

    def test_invalid_jwt(self):
        _, _, message, status_code = post({'headers': {'Authorization': 'JWT invalid'}})  # noqa: E501

        self.assertEqual(message, 'invalid auth token')
        self.assertEqual(status_code, 401)

    def test_no_permission(self):
        id = db.table('user').insert_get_id({'name': 'tester'})
        jwt = encode({'user_id': id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        _, _, message, status_code = post({'headers': {'Authorization': 'JWT {}'.format(jwt)}})  # noqa: E501

        self.assertEqual(message, 'no secret')
        self.assertEqual(status_code, 403)

    def test_post_by_accept_invite(self):
        grantee_id = db.table('user').insert_get_id({'name': 'grantee'})
        db.table('user_role').insert(type='author', secret='secret')  # noqa: E501
        grantee_jwt = encode({'user_id': grantee_id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        data, _, message, status_code = post({'headers': {'Authorization': 'JWT {}'.format(grantee_jwt)}, 'body': json.dumps({'secret': 'secret'})})  # noqa: E501

        self.assertEqual(message, None)
        self.assertEqual(status_code, 201)
        self.assertEqual(data['type'], 'author')
        self.assertEqual(data['status'], 'active')
        self.assertIsNotNone(data['secret'])
        self.assertEqual(data['user_id'], grantee_id)
        self.assertEqual(db.table('user_role').where('grantor_id', grantee_id).count(), 3)

    def test_invalid_secret(self):
        grantee_id = db.table('user').insert_get_id({'name': 'grantee'})
        db.table('user_role').insert(type='author', secret='secret')  # noqa: E501
        grantee_jwt = encode({'user_id': grantee_id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        data, _, message, status_code = post({'headers': {'Authorization': 'JWT {}'.format(grantee_jwt)}, 'body': json.dumps({'secret': 'invalid secret'})})  # noqa: E501

        self.assertEqual(message, 'invalid secret')
        self.assertEqual(status_code, 401)

    def test_already_exists_role(self):
        db.table('user_role').insert(user_id=1, type='author', status='active')  # noqa: E501
        db.table('user_role').insert(user_id=2, secret='secret', type='author', status='active')  # noqa: E501
        jwt = encode({'user_id': 2}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        data, _, message, status_code = post({'headers': {'Authorization': 'JWT {}'.format(jwt)}, 'body': json.dumps({'secret': 'secret'})})  # noqa: E501

        self.assertEqual(message, 'already exists role (author)')
        self.assertEqual(status_code, 401)

    def test_already_granted_role(self):
        db.table('user_role').insert(user_id=1, secret='secret', type='author', status='active')  # noqa: E501
        jwt = encode({'user_id': 2}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        data, _, message, status_code = post({'headers': {'Authorization': 'JWT {}'.format(jwt)}, 'body': json.dumps({'secret': 'secret'})})  # noqa: E501

        self.assertEqual(message, 'already granted role')
        self.assertEqual(status_code, 401)

    def test_present_role(self):
        db.table('user_role').insert(user_id=1, type='admin', status='active')  # noqa: E501
        jwt = encode({'user_id': 1}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        data, _, message, status_code = post({'headers': {'Authorization': 'JWT {}'.format(jwt)}, 'body': json.dumps({'user_id': 2})})  # noqa: E501

        role = db.table('user_role').where('user_id', 2).first()

        self.assertEqual(role['user_id'], 2)
        self.assertEqual(role['grantor_id'], 1)
        self.assertEqual(role['type'], 'author')
        self.assertEqual(role['status'], 'active')
        self.assertEqual(status_code, 201)

    def test_present_invitation(self):
        db.table('user_role').insert(user_id=1, type='admin', status='active')  # noqa: E501
        jwt = encode({'user_id': 1}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        data, _, message, status_code = post({'headers': {'Authorization': 'JWT {}'.format(jwt)}, 'body': json.dumps({'grantor_id': 2, 'count': 100})})  # noqa: E501

        count = (
            db.table('user_role')
            .where('grantor_id', 2)
            .where('status', 'pending')
            .where_not_null('secret')
            .where('type', 'author')
            .where_null('user_id')
            .count()
        )

        self.assertEqual(count, 5)
