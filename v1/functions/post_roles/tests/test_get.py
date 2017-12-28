import unittest
from post_roles.methods.get import get
from post_roles.methods.contrib.db import db

class GetSuite(unittest.TestCase):
    def tearDown(self):
        db.table('user').truncate()
        db.table('post_role').truncate()

    def test_get(self):
        db.table('post_role').insert_get_id({'secret': 'secret'})
        user_id = db.table('user').insert_get_id({'name': 'tester'})

        e = {'queryStringParameters': {'secret': 'secret'}}
        data, meta, message, status_code = get(e)

        self.assertEqual(meta, None)
        self.assertEqual(message, None)
        self.assertEqual(status_code, 200)
        self.assertTrue(len(data), 1)
        self.assertTrue('id' in data[0])
        self.assertTrue('user_id' in data[0])
        self.assertTrue('created_at' in data[0])
        self.assertTrue('updated_at' in data[0])

    def test_invalid_secret(self):
        e = {'queryStringParameters': {'secret': None}}
        _, _, _, status_code = get(e)

        self.assertEqual(status_code, 403)
