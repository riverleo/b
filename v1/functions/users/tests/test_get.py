import unittest
from users.methods.get import get
from users.methods.contrib.db import db


class GetCase(unittest.TestCase):
    def tearDown(self):
        db.table('user').truncate()
        db.table('action').truncate()

    def test_fetching(self):
        data, _, _, _ = get()
        self.assertEqual(len(data), 0)

        db.table('user').insert(name='test-1')

        data, _, _, _ = get()
        self.assertEqual(len(data), 1)

    def test_marshaling(self):
        db.table('user').insert(name='test-1')

        data, _, _, _ = get()
        self.assertTrue('id' in data[0])
        self.assertTrue('name' in data[0])
        self.assertTrue('lang' in data[0])
        self.assertTrue('country' in data[0])

    def test_paging(self):
        for i in range(30):
            db.table('user').insert(name='test-{}'.format(i))

        data, _, message, _ = get()
        self.assertEqual(message, None)
        self.assertEqual(len(data), 20)  # maximum data size is 20.

        data, _, _, _ = get(e={'queryStringParameters': {'per': '3'}})
        self.assertEqual(len(data), 3)

        data, _, _, _ = get(e={'queryStringParameters': {'per': '100'}})
        self.assertEqual(len(data), 20)  # max per is 20 even if exceed.

        prev, _, _, _ = get(e={'queryStringParameters': {'per': '10'}})  # noqa: E501
        data, _, _, _ = get(e={'queryStringParameters': {'page': '2', 'per': '3'}})  # noqa: E501
        self.assertEqual(prev[3], data[0])

        data, _, _, _ = get(e={'queryStringParameters': {'page': '10', 'per': '10'}})  # noqa: E501
        self.assertEqual(len(data), 0)

    def test_always_return_list(self):
        data, _, _, _ = get()

        self.assertEqual(type(data), list)
