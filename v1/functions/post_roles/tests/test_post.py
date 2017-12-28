import json
import unittest
from jwt import encode
from post_roles.methods.post import post, SECRET
from post_roles.methods.contrib.db import db


class PostSuite(unittest.TestCase):
    def tearDown(self):
        db.table('user').truncate()
        db.table('link').truncate()
        db.table('post').truncate()
        db.table('user_role').truncate()
        db.table('post_role').truncate()

    def test_invalid_jwt(self):
        _, _, message, status_code = post({'headers': {'Authorization': 'JWT invalid'}})  # noqa: E501

        self.assertEqual(message, 'invalid auth token')
        self.assertEqual(status_code, 401)

    def test_no_permission(self):
        user_id = db.table('user').insert_get_id({'name': 'tester'})
        jwt = encode({'user_id': user_id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        _, _, message, status_code = post({
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
        _, _, message, status_code = post({
            'headers': {'Authorization': 'JWT {}'.format(jwt)},
            'body': json.dumps({
                'type': 'invalid type',
                'user_id': user_id,
                'post_id': 3,
            }),
        })

        self.assertEqual(message, 'params is invalid or the value is empty')
        self.assertEqual(status_code, 403)

    def test_post_by_invite(self):
        user_id = db.table('user').insert_get_id({'name': 'tester'})
        post_id = db.table('post').insert_get_id({'key': 'key', 'title': 'new post'})
        db.table('post_role').insert(user_id=user_id, post_key='key', type='author', status='active')
        jwt = encode({'user_id': user_id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        data, _, message, status_code = post({
            'headers': {'Authorization': 'JWT {}'.format(jwt)},
            'body': json.dumps({'post_key': 'key', 'type': 'author'}),
        })  # noqa: E501

        self.assertEqual(message, None)
        self.assertEqual(status_code, 201)
        self.assertEqual(data['type'], 'author')
        self.assertEqual(data['status'], 'pending')
        self.assertTrue(data['link'].startswith('scdc.co'))
        self.assertIsNotNone(data['secret'])
        self.assertIsNone(data['user_id'])
        self.assertEqual(data['post_key'], 'key')
        self.assertEqual(data['grantor_id'], user_id)

    def test_post_by_accept_invite(self):
        grantor_id = db.table('user').insert_get_id({'name': 'grantor'})
        grantee_id = db.table('user').insert_get_id({'name': 'grantee'})
        db.table('post').insert({'key': 'post_key', 'title': 'new post'})
        db.table('post_role').insert(user_id=grantor_id, post_key='post_key', type='author', status='active')
        grantor_jwt = encode({'user_id': grantor_id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        grantee_jwt = encode({'user_id': grantee_id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        data, _, _, _ = post({'headers': {'Authorization': 'JWT {}'.format(grantor_jwt)}, 'body': json.dumps({'post_key': 'post_key', 'type': 'author'})})  # noqa: E501
        data, _, message, status_code = post({'headers': {'Authorization': 'JWT {}'.format(grantee_jwt)}, 'body': json.dumps({'secret': data['secret']})})  # noqa: E501

        self.assertEqual(message, None)
        self.assertEqual(status_code, 200)
        self.assertEqual(data['type'], 'author')
        self.assertEqual(data['status'], 'active')
        self.assertIsNotNone(data['secret'])
        self.assertEqual(data['user_id'], grantee_id)
        self.assertEqual(data['grantor_id'], grantor_id)

    def test_invalid_secret(self):
        db.table('post_role').insert(secret='valid secret', type='author', status='pending')
        grantee_id = db.table('user').insert_get_id({'name': 'grantee'})
        grantee_jwt = encode({'user_id': grantee_id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        data, _, message, status_code = post({'headers': {'Authorization': 'JWT {}'.format(grantee_jwt)}, 'body': json.dumps({'secret': 'invalid secret'})})  # noqa: E501

        self.assertEqual(message, 'invalid secret')
        self.assertEqual(status_code, 401)

    def test_already_granted_role(self):
        db.table('post_role').insert(user_id=1, secret='valid secret', type='author', status='active')
        grantee_id = db.table('user').insert_get_id({'name': 'grantee'})
        grantee_jwt = encode({'user_id': grantee_id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        data, _, message, status_code = post({'headers': {'Authorization': 'JWT {}'.format(grantee_jwt)}, 'body': json.dumps({'secret': 'valid secret'})})  # noqa: E501

        self.assertEqual(message, 'already granted role')
        self.assertEqual(status_code, 401)

    def test_post(self):
        db.table('post').insert({'key': 'key', 'title': 'new post'})
        grantor_id = db.table('user').insert_get_id({'name': 'grantor'})
        grantee_id = db.table('user').insert_get_id({'name': 'grantee'})
        db.table('post_role').insert(post_key='key', user_id=grantor_id, type='author', status='active')  # noqa: E501
        jwt = encode({'user_id': grantor_id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        data, _, message, status_code = post({
            'headers': {'Authorization': 'JWT {}'.format(jwt)},
            'body': json.dumps({
                'post_key': 'key',
                'user_id': grantee_id,
                'type': 'author',
            })
        })

        self.assertIsNone(message)
        self.assertEqual(status_code, 201)
        self.assertEqual(data['user_id'], grantee_id)
        self.assertEqual(data['status'], 'active') 
        self.assertEqual(data['type'], 'author') 

    def test_grant_author_by_no_permission(self):
        db.table('post').insert({'key': 'key', 'title': 'new post'})
        grantor_id = db.table('user').insert_get_id({'name': 'grantor'})
        grantee_id = db.table('user').insert_get_id({'name': 'grantee'})
        db.table('post_role').insert(post_key='key', user_id=grantor_id, type='assistant', status='active')  # noqa: E501
        jwt = encode({'user_id': grantor_id}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        _, _, message, status_code = post({
            'headers': {'Authorization': 'JWT {}'.format(jwt)},
            'body': json.dumps({
                'user_id': grantee_id,
                'type': 'author',
            })
        })

        self.assertEqual(message, 'no permission')
        self.assertEqual(status_code, 401)
