import json
import unittest
from me import handler
from props import set_props
from contrib import db, jwt_encode, new_id, password


class MeSuite(unittest.TestCase):
    def setUp(self):
        db.table('user').truncate()
        db.table('userRole').truncate()
        db.table('userProperty').truncate()

    def tearDown(self):
        db.table('user').truncate()
        db.table('userRole').truncate()
        db.table('userProperty').truncate()

    def test_me_by_jwt(self):
        user_id = new_id()
        db.table('user').insert(id=user_id)
        set_props(user_id, props={'key': 'value'})
        encoded = jwt_encode(user_id)

        res = handler({
            'body': json.dumps({'props': ['key', 'anonymous']}),
            'headers': {'Authorization': 'Bearer {}'.format(encoded)},
        }, None)

        body = json.loads(res['body'])

        self.assertEqual(res['statusCode'], 200)
        self.assertEqual(body['data']['id'], user_id)
        self.assertEqual(body['data']['roles'], [])
        self.assertEqual(body['data']['props']['key'], 'value')
        self.assertIsNone(body['data']['props']['anonymous'])

    def test_me_with_roles(self):
        user_id = new_id()
        db.table('user').insert(id=user_id)
        set_props(user_id, props={'key': 'value'})
        db.table('userRole').insert({'userId': user_id, 'type': 'admin'})
        encoded = jwt_encode(user_id)

        res = handler({
            'body': json.dumps({'props': ['key', 'anonymous']}),
            'headers': {'Authorization': 'Bearer {}'.format(encoded)},
        }, None)

        body = json.loads(res['body'])

        self.assertEqual(res['statusCode'], 200)
        self.assertEqual(body['data']['id'], user_id)
        self.assertEqual(body['data']['roles'], ['admin'])
        self.assertEqual(body['data']['props']['key'], 'value')
        self.assertIsNone(body['data']['props']['anonymous'])

    def test_me_by_username_and_password(self):
        user_id = new_id()
        db.table('user').insert(id=user_id)
        set_props(user_id, props={
            'key': 'value',
            'username': 'riverleo',
            'password': password('password'),
        }, unique=True)

        res = handler({
            'body': json.dumps({
                'username': 'riverleo',
                'password': 'password',
                'props': ['key', 'anonymous'],
            }),
        }, None)

        body = json.loads(res['body'])

        self.assertEqual(res['statusCode'], 200)
        self.assertEqual(body['data']['id'], user_id)
        self.assertIsNotNone(body['data']['ssid'])
        self.assertEqual(body['data']['props']['key'], 'value')
        self.assertIsNone(body['data']['props']['anonymous'])

        res = handler({
            'queryStringParameters': {
                'username': 'riverleo',
                'password': 'password',
                'props': 'key,anonymous',
            },
        }, None)

        body = json.loads(res['body'])

        self.assertEqual(res['statusCode'], 200)
        self.assertEqual(body['data']['id'], user_id)
        self.assertIsNotNone(body['data']['ssid'])
        self.assertEqual(body['data']['props']['key'], 'value')
        self.assertIsNone(body['data']['props']['anonymous'])

    def test_me_by_email_and_password(self):
        user_id = new_id()
        db.table('user').insert(id=user_id)
        set_props(user_id, props={
            'key': 'value',
            'email': 'riverleo@wslo.co',
            'password': password('password'),
        }, unique=True)

        res = handler({
            'body': json.dumps({
                'email': 'riverleo@wslo.co',
                'password': 'password',
                'props': ['key', 'anonymous'],
            }),
        }, None)

        body = json.loads(res['body'])

        self.assertEqual(res['statusCode'], 200)
        self.assertEqual(body['data']['id'], user_id)
        self.assertIsNotNone(body['data']['ssid'])
        self.assertEqual(body['data']['props']['key'], 'value')
        self.assertIsNone(body['data']['props']['anonymous'])

        res = handler({
            'queryStringParameters': {
                'email': 'riverleo@wslo.co',
                'password': 'password',
                'props': 'key,anonymous',
            },
        }, None)

        body = json.loads(res['body'])

        self.assertEqual(res['statusCode'], 200)
        self.assertEqual(body['data']['id'], user_id)
        self.assertIsNotNone(body['data']['ssid'])
        self.assertEqual(body['data']['props']['key'], 'value')
        self.assertIsNone(body['data']['props']['anonymous'])
