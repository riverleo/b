import unittest
from posts.methods.contrib.db import db
from posts.methods.get_by_id import get_by_id

class GetByIdSuite(unittest.TestCase):
    def tearDown(self):
        db.table('user').truncate()
        db.table('post').truncate()
        db.table('page').truncate()
        db.table('chapter').truncate()
        db.table('post_role').truncate()

    def test_get(self):
        post_id = db.table('post').insert_get_id({'title': 'Post', 'key': 'key'})
        user_id = db.table('user').insert_get_id({'name': 'tester'})
        db.table('post_role').insert({'post_key': 'key', 'user_id': user_id, 'type': 'author'})
        db.table('page').insert(post_key='key')
        db.table('page').insert(post_key='key')
        db.table('page').insert(post_key='key')
        db.table('chapter').insert(post_key='key', title='Chapter')
        db.table('chapter').insert(post_key='key', title='Chapter')

        e = {'pathParameters': {'id': post_id}}
        data, meta, message, status_code = get_by_id(e)

        self.assertTrue('id' in data)
        self.assertTrue('key' in data)
        self.assertTrue('title' in data)
        self.assertTrue('created_at' in data)
        self.assertTrue('updated_at' in data)
        self.assertEqual(len(data['pages']), 3)
        self.assertEqual(len(data['chapters']), 2)
        self.assertEqual(len(data['roles']), 1)
        self.assertEqual(data['roles'][0]['id'], post_id)
        self.assertEqual(data['roles'][0]['type'], 'author')
        self.assertEqual(data['roles'][0]['username'], 'tester')
        self.assertEqual(meta, None)
        self.assertEqual(message, None)
        self.assertEqual(status_code, 200)

    def test_404(self):
        e = {'pathParameters': {'id': 3842}}
        _, _, _, status_code = get_by_id(e)

        self.assertEqual(status_code, 404)
