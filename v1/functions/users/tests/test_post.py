import jwt
import json
import unittest
from users.methods.post import post, SECRET
from users.methods.contrib.db import db


class PostCase(unittest.TestCase):
    def tearDown(self):
        db.table('user').truncate()
        db.table('action').truncate()

    def test_create(self):
        body = {'email': 'tester@email.com', 'name': 'tester', 'password': 'password'}  # noqa: E501
        data, _, message, status_code = post(e={'body': json.dumps(body)})

        self.assertTrue(data)
        self.assertTrue('id' in data)
        self.assertTrue('jwt' in data)
        self.assertTrue('password' not in data)
        self.assertEqual(data.get('name'), 'tester')
        self.assertEqual(data.get('email'), 'tester@email.com')
        self.assertEqual(jwt.decode(data['jwt'], SECRET, algorithms=['HS256']), {'user_id': 1})  # noqa: E501
        self.assertEqual(message, None)
        self.assertEqual(status_code, 201)

    def test_duplicate_email(self):
        body = {'email': 'tester@email.com', 'password': 'password'}  # noqa: E501
        post(e={'body': json.dumps(body)})
        data, _, message, status_code = post(e={'body': json.dumps(body)})  # noqa: E501

        self.assertEqual(len(db.table('user').get()), 1)
        self.assertTrue('id' in data)
        self.assertTrue('jwt' in data)
        self.assertTrue('password' not in data)
        self.assertEqual(message, None)
        self.assertEqual(status_code, 201)

    def test_invalid_password(self):
        body = {'email': 'tester@email.com', 'name': 'tester', 'password': 'password'}  # noqa: E501
        post(e={'body': json.dumps(body)})

        body = {'email': 'tester@email.com', 'name': 'tester', 'password': 'invalid_password'}  # noqa: E501
        data, meta, message, status_code = post(e={'body': json.dumps(body)})

        self.assertEqual(data, None)
        self.assertEqual(meta, None)
        self.assertEqual(message, 'params are invalid or the value is empty')
        self.assertEqual(status_code, 403)
