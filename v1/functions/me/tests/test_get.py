import unittest
from jwt import encode
from me.methods.get import get, SECRET
from me.methods.contrib.db import db


class GetCase(unittest.TestCase):
    def tearDown(self):
        db.table('user').truncate()
        db.table('user_role').truncate()

    def test_invalid_jwt(self):
        _, _, message, status_code = get({'headers': {'Authorization': 'JWT invalid'}})  # noqa: E501

        self.assertEqual(message, 'invalid auth token')
        self.assertEqual(status_code, 401)


    def test_get(self):
        id_ = db.table('user').insert_get_id({'name': 'tester'})
        db.table('user_role').insert(user_id=id_, type='admin', status='active')
        db.table('user_role').insert(user_id=id_, type='author', status='active')
        db.table('user_role').insert(grantor_id=id_, type='author', status='pending')
        db.table('user_role').insert(grantor_id=2, type='author', status='pending')
        jwt = encode({'user_id': id_}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501
        data, meta, message, status_code = get({'headers': {'Authorization': 'JWT {}'.format(jwt)}})  # noqa: E501

        self.assertEqual(data['id'], id_)
        self.assertEqual(data['roles'][0]['type'], 'admin')
        self.assertEqual(data['roles'][0]['user_id'], id_)
        self.assertNotEqual(data['roles'][0]['grantor_id'], id_)
        self.assertEqual(data['roles'][1]['type'], 'author')
        self.assertEqual(data['roles'][1]['user_id'], id_)
        self.assertNotEqual(data['roles'][1]['grantor_id'], id_)
        self.assertEqual(data['roles'][2]['type'], 'author')
        self.assertNotEqual(data['roles'][2]['user_id'], id_)
        self.assertEqual(data['roles'][2]['grantor_id'], id_)
        self.assertEqual(len(data['roles']), 3)
        self.assertIsNone(meta)
        self.assertIsNone(message)
        self.assertEqual(status_code, 200)
