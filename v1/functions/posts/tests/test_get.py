import unittest
from posts.methods.get import get
from posts.methods.contrib.db import db


class GetSuite(unittest.TestCase):
    def tearDown(Self):
        db.table('user').truncate()
        db.table('post').truncate()
        db.table('post_role').truncate()

    def test_fetching(self):
        data, _, _, _ = get()
        self.assertEqual(len(data), 0)

        db.table('post').insert(title='post-1', status='active')

        data, _, _, _ = get()
        self.assertEqual(len(data), 1)

    def test_marshaling(self):
        db.table('post').insert(title='post-1', status='active')

        data, _, _, _ = get()
        self.assertTrue('id' in data[0])
        self.assertTrue('key' in data[0])
        self.assertTrue('title' in data[0])
        self.assertTrue('created_at' in data[0])
        self.assertTrue('updated_at' in data[0])

    def test_paging(self):
        for i in range(30):
            db.table('post').insert(title='post-{}'.format(i), status='active')

        data, _, message, _ = get()
        self.assertEqual(message, None)
        self.assertEqual(len(data), 20)  # maximum data size is 20.

        data, _, _, _ = get(e={'queryStringParameters': {'per': '3'}})
        self.assertEqual(len(data), 3)

        data, _, _, _ = get(e={'queryStringParameters': {'per': '100'}})
        self.assertEqual(len(data), 20)  # max per is 20 even if exceed.

        prev, _, _, _ = get(e={'queryStringParameters': {'per': '10'}})  # noqa: E501
        data, _, _, _ = get(e={'queryStringParameters': {'per': '3', 'page': '2'}})  # noqa: E501
        self.assertEqual(prev[3], data[0])

        data, _, _, _ = get(e={'queryStringParameters': {'per': '100', 'page': '100'}})  # noqa: E501
        self.assertEqual(len(data), 0)

    def test_status_filtering(self):
        db.table('post').insert(title='post-1', status='active')
        db.table('post').insert(title='post-2', status='active')
        db.table('post').insert(title='post-3', status='draft')

        data, _, _, _ = get(e={'queryStringParameters': {'status': 'active'}})
        self.assertEqual(len(data), 2)

        data, _, _, _ = get(e={'queryStringParameters': {'status': 'draft'}})
        self.assertEqual(len(data), 1)

    def test_user_filtering(self):
        id = db.table('post').insert_get_id({'key': 'key1', 'title': 'post-1'})
        db.table('post_role').insert(user_id=1, post_key='key1')
        id = db.table('post').insert_get_id({'key': 'key2', 'title': 'post-2'})
        db.table('post_role').insert(user_id=1, post_key='key2')
        id = db.table('post').insert_get_id({'key': 'key3', 'title': 'post-3'})
        db.table('post_role').insert(user_id=2, post_key='key3')

        data, _, _, _ = get(e={'queryStringParameters': {'user_id': 1}})
        self.assertEqual(len(data), 2)

        data, _, _, _ = get(e={'queryStringParameters': {'user_id': 2}})
        self.assertEqual(len(data), 1)

    def test_always_return_list(self):
        data, _, _, _ = get()

        self.assertEqual(type(data), list)
        pass
